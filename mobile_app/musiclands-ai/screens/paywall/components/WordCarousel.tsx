import React, { useEffect, useRef } from 'react';
import { View, Text, Animated } from 'react-native';
import { paywallStyles } from '../styles/paywall.styles';
import { usePaywallStore } from '@/stores/paywall.store';

const CAROUSEL_WORDS = [
  'VIBES',
  'SLAPS',
  'FIRE',
  'BUSSIN',
  'HITS DIFFERENT',
  'NO CAP',
  'LOWKEY ICONIC',
  'IT\'S GIVING MAIN CHARACTER'
];

export const WordCarousel: React.FC = () => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const currentWordIndex = useRef(0);
  const { currentWord, setCurrentWord } = usePaywallStore();

  useEffect(() => {
    const animateWords = () => {
      Animated.sequence([
        Animated.timing(fadeAnim, {
          toValue: 0,
          duration: 500,
          useNativeDriver: true,
        }),
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 500,
          useNativeDriver: true,
        })
      ]).start();

      currentWordIndex.current = (currentWordIndex.current + 1) % CAROUSEL_WORDS.length;
      setCurrentWord(CAROUSEL_WORDS[currentWordIndex.current]);
    };

    const wordInterval = setInterval(animateWords, 2500);

    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start();

    return () => clearInterval(wordInterval);
  }, [fadeAnim, setCurrentWord]);

  return (
    <View style={paywallStyles.carouselSection}>
      <Text style={paywallStyles.carouselLabel}>
        This lineup is
      </Text>
      <Animated.View 
        style={[
          paywallStyles.carouselWordContainer,
          { opacity: fadeAnim }
        ]}
      >
        <Text style={paywallStyles.carouselWord}>
          {currentWord}
        </Text>
      </Animated.View>
    </View>
  );
};