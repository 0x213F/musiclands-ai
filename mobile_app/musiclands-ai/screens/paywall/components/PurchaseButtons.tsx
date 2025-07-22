import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { paywallStyles } from '../styles/paywall.styles';
import { usePaywallStore } from '@/stores/paywall.store';
import { iapService } from '@/services/purchases';

export const PurchaseButtons: React.FC = () => {
  const router = useRouter();
  const [isDevelopment, setIsDevelopment] = useState(false);
  const {
    isLoading,
    isPurchasing,
    purchaseProduct,
    restorePurchases,
    getProductPrice
  } = usePaywallStore();

  useEffect(() => {
    // Check if we're in development mode after initialization
    const checkDevelopmentMode = () => {
      setIsDevelopment(iapService.isDevelopment());
    };
    
    // Small delay to let initialization complete
    const timer = setTimeout(checkDevelopmentMode, 1000);
    return () => clearTimeout(timer);
  }, []);

  const handlePurchase = (productId: string) => {
    purchaseProduct(productId, () => router.push('/chat'));
  };

  const handleRestore = () => {
    restorePurchases(() => router.push('/chat'));
  };

  if (isLoading) {
    return (
      <View style={paywallStyles.loadingContainer}>
        <ActivityIndicator size="large" color="white" />
        <Text style={paywallStyles.loadingText}>
          {isDevelopment ? 'Setting up development mode...' : 'Loading purchase options...'}
        </Text>
      </View>
    );
  }

  return (
    <View style={paywallStyles.purchaseSection}>
      <TouchableOpacity
        onPress={() => handlePurchase('premium_3day')}
        disabled={isPurchasing !== null}
        style={[
          paywallStyles.primaryButton,
          isPurchasing === 'premium_3day' && paywallStyles.primaryButtonDisabled
        ]}
      >
        {isPurchasing === 'premium_3day' ? (
          <ActivityIndicator color="white" />
        ) : (
          <>
            <Text style={paywallStyles.buttonTextPrimary}>
              3 Days for {getProductPrice('premium_3day')}
            </Text>
            <Text style={paywallStyles.buttonSubtext}>
              Full send weekend vibes ✨
            </Text>
          </>
        )}
      </TouchableOpacity>
      
      <TouchableOpacity
        onPress={() => handlePurchase('premium_1day')}
        disabled={isPurchasing !== null}
        style={[
          paywallStyles.secondaryButton,
          isPurchasing === 'premium_1day' && paywallStyles.secondaryButtonDisabled
        ]}
      >
        {isPurchasing === 'premium_1day' ? (
          <ActivityIndicator color="white" />
        ) : (
          <>
            <Text style={paywallStyles.buttonTextSecondary}>
              1 Day for {getProductPrice('premium_1day')}
            </Text>
            <Text style={paywallStyles.buttonSubtext}>
              Day one energy only 🔥
            </Text>
          </>
        )}
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={paywallStyles.restoreButton}
        onPress={handleRestore}
        disabled={isLoading}
      >
        <Text style={paywallStyles.restoreText}>
          Restore Previous Purchases
        </Text>
      </TouchableOpacity>
      
      {isDevelopment && (
        <View style={{ alignItems: 'center', marginTop: 8 }}>
          <Text style={{ color: 'rgba(255,255,255,0.5)', fontSize: 11, fontStyle: 'italic' }}>
            Development Mode - Mock Purchases
          </Text>
        </View>
      )}
    </View>
  );
};