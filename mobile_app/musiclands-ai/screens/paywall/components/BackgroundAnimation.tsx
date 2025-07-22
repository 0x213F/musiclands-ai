import React, { useEffect, useRef } from 'react';
import { View, Animated } from 'react-native';
import { paywallStyles } from '../styles/paywall.styles';

export const BackgroundAnimation: React.FC = () => {
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 20000,
        useNativeDriver: true,
      })
    ).start();
  }, [rotateAnim]);

  const spin = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <View style={paywallStyles.backgroundOverlay}>
      <Animated.View
        style={[
          paywallStyles.backgroundCircleLarge,
          { transform: [{ rotate: spin }] }
        ]}
      />
      <Animated.View
        style={[
          paywallStyles.backgroundCircleSmall,
          { transform: [{ rotate: spin }] }
        ]}
      />
    </View>
  );
};