import { create } from 'zustand';
import { Product } from 'react-native-iap';
import { Alert } from 'react-native';
import { iapService } from '@/services/purchases';

interface PaywallState {
  // State
  currentWord: string;
  products: Product[];
  isLoading: boolean;
  isPurchasing: string | null;
  
  // Actions
  setCurrentWord: (word: string) => void;
  setProducts: (products: Product[]) => void;
  setIsLoading: (loading: boolean) => void;
  setIsPurchasing: (productId: string | null) => void;
  
  // Async actions
  loadProducts: () => Promise<void>;
  purchaseProduct: (productId: string, onSuccess: () => void) => Promise<void>;
  restorePurchases: (onSuccess: () => void) => Promise<void>;
  
  // Getters
  getProductPrice: (productId: string) => string;
  getProductTitle: (productId: string) => string;
}

export const usePaywallStore = create<PaywallState>((set, get) => ({
  // Initial state
  currentWord: 'VIBES',
  products: [],
  isLoading: false,
  isPurchasing: null,

  // Setters
  setCurrentWord: (word) => set({ currentWord: word }),
  setProducts: (products) => set({ products }),
  setIsLoading: (loading) => set({ isLoading: loading }),
  setIsPurchasing: (productId) => set({ isPurchasing: productId }),

  // Load products from IAP service
  loadProducts: async () => {
    const { setIsLoading, setProducts } = get();
    
    try {
      setIsLoading(true);
      const availableProducts = await iapService.getProducts();
      setProducts(availableProducts);
    } catch (error: any) {
      console.error('Failed to load products:', error);
      
      // Don't show error alert for development mode
      const isIAPUnavailable = error.code === 'E_IAP_NOT_AVAILABLE' || 
                               error.message?.includes('IAP_NOT_AVAILABLE') ||
                               error.message?.includes('not available');
                               
      if (!isIAPUnavailable) {
        Alert.alert(
          'Error',
          'Failed to load purchase options. Please try again later.'
        );
      }
    } finally {
      setIsLoading(false);
    }
  },

  // Purchase a product
  purchaseProduct: async (productId, onSuccess) => {
    const { products, setIsPurchasing } = get();
    
    if (products.length === 0) {
      Alert.alert('Error', 'No purchase options available');
      return;
    }

    try {
      setIsPurchasing(productId);
      
      // Purchase the product
      await iapService.purchaseProduct(productId);
      
      // Check if purchase was successful
      const customerInfo = await iapService.getCustomerInfo();
      
      if (iapService.hasActivePremium(customerInfo)) {
        Alert.alert(
          'Success! 🎉',
          'Welcome to Music Land AI Premium! Let\'s get this festival started!',
          [
            {
              text: 'Let\'s Go!',
              onPress: onSuccess,
            },
          ]
        );
      } else {
        Alert.alert('Purchase Incomplete', 'Please try again or contact support.');
      }
    } catch (error: any) {
      console.error('Purchase failed:', error);
      
      if (error.code === 'E_USER_CANCELLED') {
        // User cancelled, no need to show error
        return;
      }
      
      // Don't show error alert for development mode
      const isIAPUnavailable = error.code === 'E_IAP_NOT_AVAILABLE' || 
                               error.message?.includes('IAP_NOT_AVAILABLE') ||
                               error.message?.includes('not available');
                               
      if (!isIAPUnavailable) {
        Alert.alert(
          'Purchase Failed',
          error.message || 'Something went wrong. Please try again.'
        );
      }
    } finally {
      setIsPurchasing(null);
    }
  },

  // Restore purchases
  restorePurchases: async (onSuccess) => {
    const { setIsLoading } = get();
    
    try {
      setIsLoading(true);
      await iapService.restorePurchases();
      const customerInfo = await iapService.getCustomerInfo();
      
      if (iapService.hasActivePremium(customerInfo)) {
        Alert.alert(
          'Purchases Restored! 🎉',
          'Your premium access has been restored!',
          [
            {
              text: 'Continue',
              onPress: onSuccess,
            },
          ]
        );
      } else {
        Alert.alert(
          'No Purchases Found',
          'We couldn\'t find any previous purchases to restore.'
        );
      }
    } catch (error: any) {
      console.error('Restore failed:', error);
      
      // Don't show error alert for development mode
      const isIAPUnavailable = error.code === 'E_IAP_NOT_AVAILABLE' || 
                               error.message?.includes('IAP_NOT_AVAILABLE') ||
                               error.message?.includes('not available');
                               
      if (!isIAPUnavailable) {
        Alert.alert('Restore Failed', 'Unable to restore purchases. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  },

  // Get product price with fallback
  getProductPrice: (productId) => {
    const { products } = get();
    if (products.length === 0) {
      return productId === 'premium_3day' ? '$4.99' : '$1.99';
    }
    const product = products.find(p => p.productId === productId);
    return product?.localizedPrice || (productId === 'premium_3day' ? '$4.99' : '$1.99');
  },

  // Get product title with fallback
  getProductTitle: (productId) => {
    const { products } = get();
    if (products.length === 0) return 'Premium Access';
    const product = products.find(p => p.productId === productId);
    return product?.title || 'Premium Access';
  },
}));