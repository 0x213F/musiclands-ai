import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, ScrollView, Alert, Text, Modal } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useThemeColor } from '@/hooks/useThemeColor';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { apiService } from '@/services/api';

const SAMPLE_QUESTIONS = [
  "Should I stay here or check out another stage?",
  "Which artist has better vibes for dancing?",
  "I'm dead tired, where can I chill for a bit?",
  "What artist should I absolutely not miss?",
  "How do I get to the main stage without crowds?",
  "Where are the cleanest bathrooms rn?",
];

export default function ChatScreen() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<Array<{id: string, text: string, isUser: boolean}>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showInfoModal, setShowInfoModal] = useState(false);
  
  const backgroundColor = useThemeColor({}, 'background');
  const textColor = useThemeColor({}, 'text');
  const tintColor = useThemeColor({}, 'tint');
  const cardColor = useThemeColor({ light: '#f5f5f5', dark: '#2c2c2c' }, 'background');

  const handleSendMessage = async (message?: string) => {
    const messageText = message || inputText.trim();
    if (!messageText || isLoading) return;

    const newMessage = {
      id: Date.now().toString(),
      text: messageText,
      isUser: true,
    };

    setMessages(prev => [...prev, newMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await apiService.sendChatMessage(messageText);
      
      const aiResponse = {
        id: response.message_id,
        text: response.response,
        isUser: false,
      };
      
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('API Error:', error);
      
      // Fallback response on error
      const errorResponse = {
        id: (Date.now() + 1).toString(),
        text: "Sorry bestie, I'm having trouble connecting right now 😅 Try again in a sec!",
        isUser: false,
      };
      
      setMessages(prev => [...prev, errorResponse]);
      
      // Show user-friendly error
      Alert.alert(
        "Connection Issue", 
        "Having trouble reaching the festival AI. Check your internet connection!"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = (question: string) => {
    handleSendMessage(question);
  };

  return (
    <SafeAreaView className="flex-1" style={{ backgroundColor }}>
      <View className="px-5 py-4 border-b border-gray-300/20 flex-row items-center justify-between">
        <View className="flex-1" />
        <Text 
          className="text-2xl font-bold flex-1 text-center" 
          style={{ color: textColor }}
        >
          Musiclands AI
        </Text>
        <View className="flex-1 items-end">
          <TouchableOpacity
            onPress={() => setShowInfoModal(true)}
            className="p-2"
          >
            <IconSymbol name="info.circle" size={24} color={tintColor} />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView 
        className="flex-1"
        contentContainerStyle={{ flexGrow: 1, padding: 20 }}
        showsVerticalScrollIndicator={false}
      >
        {messages.length === 0 ? (
          <View className="flex-1 justify-center items-center px-5">
            <View className="w-full gap-3">
              {SAMPLE_QUESTIONS.map((question, index) => (
                <TouchableOpacity
                  key={index}
                  className="p-4 rounded-xl items-center"
                  style={{ backgroundColor: cardColor }}
                  onPress={() => handleQuickQuestion(question)}
                  activeOpacity={0.7}
                >
                  <Text 
                    className="text-base text-center font-medium" 
                    style={{ color: textColor }}
                  >
                    {question}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        ) : (
          <View className="gap-3">
            {messages.map((message) => (
              <View
                key={message.id}
                className={`p-3 rounded-2xl max-w-4/5 ${
                  message.isUser 
                    ? 'self-end rounded-br-sm' 
                    : 'self-start rounded-bl-sm'
                }`}
                style={{
                  backgroundColor: message.isUser ? tintColor : cardColor,
                }}
              >
                <Text 
                  className="text-base leading-6"
                  style={{
                    color: message.isUser ? 'white' : textColor
                  }}
                >
                  {message.text}
                </Text>
              </View>
            ))}
            {isLoading && (
              <View
                className="p-3 rounded-2xl max-w-4/5 self-start rounded-bl-sm"
                style={{ backgroundColor: cardColor }}
              >
                <Text 
                  className="text-base leading-6 italic"
                  style={{ color: textColor }}
                >
                  Festival AI is thinking... 🤔
                </Text>
              </View>
            )}
          </View>
        )}
      </ScrollView>

      <View 
        className="flex-row px-4 py-3 items-end gap-3 mx-4 mb-4 rounded-3xl"
        style={{ backgroundColor: cardColor }}
      >
        <TextInput
          className="flex-1 text-base leading-6 py-2 px-1"
          style={{ color: textColor }}
          placeholder="Ask me about the festival..."
          placeholderTextColor={textColor + '80'}
          value={inputText}
          onChangeText={setInputText}
          multiline
          maxLength={500}
        />
        <TouchableOpacity
          className="w-9 h-9 rounded-full justify-center items-center"
          style={{
            backgroundColor: isLoading ? tintColor + '50' : tintColor,
          }}
          onPress={() => handleSendMessage()}
          activeOpacity={0.8}
          disabled={isLoading}
        >
          {isLoading ? (
            <Text className="text-white text-xs">...</Text>
          ) : (
            <IconSymbol name="arrow.up" size={20} color="white" />
          )}
        </TouchableOpacity>
      </View>

      <Modal
        visible={showInfoModal}
        animationType="slide"
        presentationStyle="pageSheet"
        onRequestClose={() => setShowInfoModal(false)}
      >
        <SafeAreaView className="flex-1" style={{ backgroundColor }}>
          <View className="px-5 py-4 border-b border-gray-300/20 flex-row items-center justify-between">
            <TouchableOpacity
              onPress={() => setShowInfoModal(false)}
              className="p-2"
            >
              <IconSymbol name="xmark" size={24} color={tintColor} />
            </TouchableOpacity>
            <Text 
              className="text-lg font-bold" 
              style={{ color: textColor }}
            >
              About
            </Text>
            <View className="w-10" />
          </View>
          
          <ScrollView className="flex-1 px-5 py-6">
            <View className="items-center mb-8">
              <IconSymbol name="music.note" size={80} color={tintColor} className="mb-4" />
              <Text 
                className="text-3xl font-bold text-center mb-2" 
                style={{ color: textColor }}
              >
                Your festival AI bestie is here! 🎵
              </Text>
              <Text 
                className="text-lg text-center opacity-70" 
                style={{ color: textColor }}
              >
                Ask me anything to make your festival experience hit different
              </Text>
            </View>

            <View className="gap-6">
              <View>
                <Text 
                  className="text-xl font-bold mb-3" 
                  style={{ color: textColor }}
                >
                  What I can help with:
                </Text>
                <View className="gap-3">
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Finding the best stages and artists to check out
                  </Text>
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Navigating the festival grounds like a pro
                  </Text>
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Discovering new music and hidden gems
                  </Text>
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Finding food, bathrooms, and chill spots
                  </Text>
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Making your festival experience absolutely iconic
                  </Text>
                </View>
              </View>

              <View>
                <Text 
                  className="text-xl font-bold mb-3" 
                  style={{ color: textColor }}
                >
                  Tips for the best results:
                </Text>
                <View className="gap-3">
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Ask specific questions about what you’re looking for
                  </Text>
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Let me know your music preferences and vibe
                  </Text>
                  <Text 
                    className="text-base opacity-80" 
                    style={{ color: textColor }}
                  >
                    • Don’t be afraid to ask follow-up questions
                  </Text>
                </View>
              </View>
            </View>
          </ScrollView>
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
}

// Removed styles - now using Tailwind classes