import React, { useEffect } from 'react';
import { View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { usePaywallStore } from '@/stores/paywall.store';
import { paywallStyles } from './styles/paywall.styles';
import {
  PaywallHeader,
  WordCarousel,
  BackgroundAnimation,
  PurchaseButtons
} from './components';

export const PaywallScreen: React.FC = () => {
  const insets = useSafeAreaInsets();
  const { loadProducts } = usePaywallStore();

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  return (
    <LinearGradient
      colors={['#FF6B9D', '#C44EFD', '#4ECFFD', '#44FFB3']}
      style={[paywallStyles.container, { paddingTop: insets.top }]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
    >
      <BackgroundAnimation />
      
      <View style={paywallStyles.mainContent}>
        <PaywallHeader />
        <WordCarousel />
        <PurchaseButtons />
      </View>
    </LinearGradient>
  );
};