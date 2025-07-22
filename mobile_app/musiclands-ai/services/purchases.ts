import {
  initConnection,
  getProducts,
  requestPurchase,
  finishTransaction,
  acknowledgePurchaseAndroid,
  purchaseErrorListener,
  purchaseUpdatedListener,
  type ProductPurchase,
  type Product,
  type PurchaseError,
  endConnection,
  clearProductsIOS,
  flushFailedPurchasesCachedAsPendingAndroid,
  getAvailablePurchases,
} from 'react-native-iap';
import { Platform, EmitterSubscription } from 'react-native';

export interface PurchasePackage {
  productId: string;
  title: string;
  description: string;
  price: string;
  currency: string;
  type: 'inapp' | 'subs';
}

export interface CustomerInfo {
  purchases: ProductPurchase[];
  hasPremium: boolean;
  premiumExpirationDate?: Date;
}

class IAPService {
  private isInitialized = false;
  private purchaseUpdateSubscription: EmitterSubscription | null = null;
  private purchaseErrorSubscription: EmitterSubscription | null = null;
  private isDevelopmentMode = false;

  // Product IDs for your in-app purchases
  private readonly productIds = [
    'premium_3day', // $4.99 for 3 days
    'premium_1day', // $1.99 for 1 day
  ];

  // Helper method to check if error is IAP not available
  private isIAPUnavailable(error: any): boolean {
    return error.code === 'E_IAP_NOT_AVAILABLE' || 
           error.message?.includes('IAP_NOT_AVAILABLE') ||
           error.message?.includes('not available');
  }

  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    try {
      // Initialize connection to app store
      await initConnection();
      
      // Clear any cached products on iOS
      if (Platform.OS === 'ios') {
        await clearProductsIOS();
      }

      // Flush failed purchases on Android
      if (Platform.OS === 'android') {
        await flushFailedPurchasesCachedAsPendingAndroid();
      }

      // Set up purchase listeners
      this.setupPurchaseListeners();

      this.isInitialized = true;
      console.log('IAP Service initialized successfully');
    } catch (error: any) {
      console.error('Failed to initialize IAP Service:', error);
      
      // If IAP is not available (simulator/development), mark as initialized anyway
      // to prevent repeated initialization attempts
      if (this.isIAPUnavailable(error)) {
        this.isInitialized = true;
        this.isDevelopmentMode = true;
        console.warn('IAP not available - running in development/simulator mode');
        return;
      }
      
      throw error;
    }
  }

  private setupPurchaseListeners(): void {
    // Purchase update listener
    this.purchaseUpdateSubscription = purchaseUpdatedListener(
      async (purchase: ProductPurchase) => {
        console.log('Purchase updated:', purchase);
        
        try {
          // Verify the purchase receipt here if needed
          
          // Finish the transaction
          await finishTransaction({ purchase, isConsumable: false });
          
          // On Android, acknowledge the purchase
          if (Platform.OS === 'android') {
            await acknowledgePurchaseAndroid({
              token: purchase.purchaseToken!,
            });
          }
          
          console.log('Purchase completed successfully');
        } catch (error) {
          console.error('Error processing purchase:', error);
        }
      }
    );

    // Purchase error listener
    this.purchaseErrorSubscription = purchaseErrorListener(
      (error: PurchaseError) => {
        console.error('Purchase error:', error);
      }
    );
  }

  async getProducts(): Promise<Product[]> {
    try {
      if (!this.isInitialized) {
        await this.initialize();
      }

      const products = await getProducts({
        skus: this.productIds,
      });

      return products;
    } catch (error: any) {
      console.error('Failed to get products:', error);
      
      // Return mock products for development/simulator
      if (this.isIAPUnavailable(error)) {
        console.warn('Returning mock products for development mode');
        return [
          {
            productId: 'premium_3day',
            price: '4.99',
            currency: 'USD',
            localizedPrice: '$4.99',
            title: '3-Day Premium Access',
            description: 'Get premium access to Music Land AI for 3 days',
          },
          {
            productId: 'premium_1day', 
            price: '1.99',
            currency: 'USD',
            localizedPrice: '$1.99',
            title: '1-Day Premium Access',
            description: 'Get premium access to Music Land AI for 1 day',
          }
        ] as Product[];
      }
      
      throw error;
    }
  }

  async purchaseProduct(productId: string): Promise<ProductPurchase> {
    try {
      if (!this.isInitialized) {
        await this.initialize();
      }

      const purchase = await requestPurchase({
        sku: productId,
        andDangerouslyFinishTransactionAutomaticallyIOS: false,
      });

      return purchase;
    } catch (error: any) {
      console.error('Purchase failed:', error);
      
      // Simulate successful purchase for development
      if (this.isIAPUnavailable(error)) {
        console.warn('Simulating successful purchase for development mode');
        return {
          productId,
          transactionId: `dev_${Date.now()}`,
          transactionDate: Date.now().toString(),
          purchaseToken: `dev_token_${Date.now()}`,
          applicationUsername: 'dev_user',
          transactionReceipt: 'dev_receipt',
        } as ProductPurchase;
      }
      
      throw error;
    }
  }

  async restorePurchases(): Promise<ProductPurchase[]> {
    try {
      if (!this.isInitialized) {
        await this.initialize();
      }

      const purchases = await getAvailablePurchases();
      console.log('Restored purchases:', purchases);
      
      return purchases;
    } catch (error: any) {
      console.error('Failed to restore purchases:', error);
      
      // Return empty array for development mode
      if (this.isIAPUnavailable(error)) {
        console.warn('No purchases to restore in development mode');
        return [];
      }
      
      throw error;
    }
  }

  async getCustomerInfo(): Promise<CustomerInfo> {
    try {
      const purchases = await this.restorePurchases();
      const activePurchases = this.filterActivePurchases(purchases);
      
      return {
        purchases: activePurchases,
        hasPremium: activePurchases.length > 0,
        premiumExpirationDate: this.getLatestExpirationDate(activePurchases),
      };
    } catch (error) {
      console.error('Failed to get customer info:', error);
      return {
        purchases: [],
        hasPremium: false,
      };
    }
  }

  private filterActivePurchases(purchases: ProductPurchase[]): ProductPurchase[] {
    const now = new Date();
    
    return purchases.filter(purchase => {
      if (!this.productIds.includes(purchase.productId)) {
        return false;
      }

      const expirationDate = this.calculateExpirationDate(purchase);
      return expirationDate ? now < expirationDate : false;
    });
  }

  private calculateExpirationDate(purchase: ProductPurchase): Date | null {
    if (!purchase.transactionDate) {
      return null;
    }

    const purchaseDate = new Date(parseInt(purchase.transactionDate, 10));
    
    // Add days based on product type
    if (purchase.productId === 'premium_3day') {
      purchaseDate.setDate(purchaseDate.getDate() + 3);
    } else if (purchase.productId === 'premium_1day') {
      purchaseDate.setDate(purchaseDate.getDate() + 1);
    }
    
    return purchaseDate;
  }

  private getLatestExpirationDate(purchases: ProductPurchase[]): Date | undefined {
    if (purchases.length === 0) return undefined;

    const expirationDates = purchases
      .map(purchase => this.calculateExpirationDate(purchase))
      .filter((date): date is Date => date !== null);

    if (expirationDates.length === 0) return undefined;

    return new Date(Math.max(...expirationDates.map(date => date.getTime())));
  }

  hasActivePremium(customerInfo: CustomerInfo): boolean {
    return customerInfo.hasPremium;
  }

  getPremiumExpirationDate(customerInfo: CustomerInfo): Date | null {
    return customerInfo.premiumExpirationDate || null;
  }

  // Public method to check if running in development mode
  isDevelopment(): boolean {
    return this.isDevelopmentMode;
  }

  async destroy(): Promise<void> {
    // Remove listeners
    if (this.purchaseUpdateSubscription) {
      this.purchaseUpdateSubscription.remove();
      this.purchaseUpdateSubscription = null;
    }
    
    if (this.purchaseErrorSubscription) {
      this.purchaseErrorSubscription.remove();
      this.purchaseErrorSubscription = null;
    }

    // End connection (skip if in development mode)
    if (!this.isDevelopmentMode) {
      try {
        await endConnection();
        console.log('IAP Service destroyed');
      } catch (error) {
        console.error('Error destroying IAP Service:', error);
      }
    }
    
    this.isInitialized = false;
  }
}

export const iapService = new IAPService();