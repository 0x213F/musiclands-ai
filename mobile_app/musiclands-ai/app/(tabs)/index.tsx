import React, { useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, Animated, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const { width, height } = Dimensions.get('window');

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

export default function HomeScreen() {
  const insets = useSafeAreaInsets();
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;
  const currentWordIndex = useRef(0);
  const [currentWord, setCurrentWord] = React.useState(CAROUSEL_WORDS[0]);

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

    Animated.loop(
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 20000,
        useNativeDriver: true,
      })
    ).start();

    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start();

    return () => clearInterval(wordInterval);
  }, []);

  const spin = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <LinearGradient
      colors={['#FF6B9D', '#C44EFD', '#4ECFFD', '#44FFB3']}
      className="flex-1"
      style={{ paddingTop: insets.top }}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
    >
      <View className="absolute inset-0 overflow-hidden">
        <Animated.View
          className="absolute w-80 h-80 rounded-full bg-white/10 -top-12 -right-24"
          style={{
            transform: [{ rotate: spin }],
          }}
        />
        <Animated.View
          className="absolute w-52 h-52 rounded-full bg-white/5 -bottom-12 -left-12"
          style={{
            transform: [{ rotate: spin }],
          }}
        />
      </View>

      <View className="flex-1 justify-between px-6 py-10 z-10">
        <View className="items-center mt-16">
          <Text className="text-2xl font-light text-white text-center tracking-widest">
            Welcome to
          </Text>
          <Text 
            className="text-4xl font-bold text-white text-center my-2" 
            style={{
              textShadowColor: 'rgba(0, 0, 0, 0.3)',
              textShadowOffset: { width: 2, height: 2 },
              textShadowRadius: 4,
            }}
          >
            Music Land AI
          </Text>
          <Text className="text-base text-white/90 text-center italic">
            Your festival bestie fr 💯
          </Text>
        </View>

        <View className="items-center justify-center flex-1">
          <Text className="text-3xl text-white font-light mb-4">
            This lineup is
          </Text>
          <Animated.View 
            className="bg-white/20 px-8 py-4 rounded-3xl border-2 border-white/30"
            style={{ opacity: fadeAnim }}
          >
            <Text 
              className="text-5xl font-bold text-white text-center tracking-widest"
              style={{
                textShadowColor: 'rgba(0, 0, 0, 0.5)',
                textShadowOffset: { width: 2, height: 2 },
                textShadowRadius: 6,
              }}
            >
              {currentWord}
            </Text>
          </Animated.View>
        </View>

        <View className="gap-4">
          <TouchableOpacity 
            className="bg-festival-red py-5 px-8 rounded-full items-center shadow-lg"
            style={{
              shadowColor: '#000',
              shadowOffset: { width: 0, height: 4 },
              shadowOpacity: 0.3,
              shadowRadius: 8,
              elevation: 8,
            }}
          >
            <Text className="text-white text-xl font-bold tracking-wide">
              3 Days for $4.99
            </Text>
            <Text className="text-white/90 text-xs mt-1">
              Full send weekend vibes ✨
            </Text>
          </TouchableOpacity>
          
          <TouchableOpacity className="bg-white/20 border-2 border-white py-5 px-8 rounded-full items-center">
            <Text className="text-white text-lg font-bold tracking-wide">
              1 Day for $1.99
            </Text>
            <Text className="text-white/90 text-xs mt-1">
              Day one energy only 🔥
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </LinearGradient>
  );
}

// Removed styles - now using Tailwind classes
