import React from 'react';
import { View, Text } from 'react-native';
import { paywallStyles } from '../styles/paywall.styles';

export const PaywallHeader: React.FC = () => {
  return (
    <View style={paywallStyles.header}>
      <Text style={paywallStyles.welcomeText}>
        Welcome to
      </Text>
      <Text style={paywallStyles.titleText}>
        Music Land AI
      </Text>
      <Text style={paywallStyles.subtitleText}>
        Your festival bestie fr 💯
      </Text>
    </View>
  );
};