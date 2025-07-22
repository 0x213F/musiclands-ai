import { StyleSheet } from 'react-native';

export const paywallStyles = StyleSheet.create({
  // Container styles
  container: {
    flex: 1,
  },
  
  backgroundOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    overflow: 'hidden',
  },
  
  mainContent: {
    flex: 1,
    justifyContent: 'space-between',
    paddingHorizontal: 24,
    paddingVertical: 40,
    zIndex: 10,
  },

  // Animated background elements
  backgroundCircleLarge: {
    position: 'absolute',
    width: 320,
    height: 320,
    borderRadius: 160,
    backgroundColor: 'rgba(255,255,255,0.1)',
    top: -48,
    right: -96,
  },
  
  backgroundCircleSmall: {
    position: 'absolute',
    width: 208,
    height: 208,
    borderRadius: 104,
    backgroundColor: 'rgba(255,255,255,0.05)',
    bottom: -48,
    left: -48,
  },

  // Header section
  header: {
    alignItems: 'center',
    marginTop: 64,
  },
  
  welcomeText: {
    fontSize: 24,
    fontWeight: '300',
    color: 'white',
    textAlign: 'center',
    letterSpacing: 2,
  },
  
  titleText: {
    fontSize: 36,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginVertical: 8,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 4,
  },
  
  subtitleText: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.9)',
    textAlign: 'center',
    fontStyle: 'italic',
  },

  // Middle section (word carousel)
  carouselSection: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
  },
  
  carouselLabel: {
    fontSize: 28,
    color: 'white',
    fontWeight: '300',
    marginBottom: 16,
  },
  
  carouselWordContainer: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 24,
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.3)',
  },
  
  carouselWord: {
    fontSize: 48,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    letterSpacing: 3,
    textShadowColor: 'rgba(0, 0, 0, 0.5)',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 6,
  },

  // Purchase section
  purchaseSection: {
    gap: 16,
  },
  
  loadingContainer: {
    paddingVertical: 32,
    alignItems: 'center',
  },
  
  loadingText: {
    color: 'white',
    marginTop: 8,
  },

  // Button styles
  primaryButton: {
    paddingVertical: 20,
    paddingHorizontal: 32,
    borderRadius: 25,
    alignItems: 'center',
    backgroundColor: '#FF1744',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  
  primaryButtonDisabled: {
    opacity: 0.7,
  },
  
  secondaryButton: {
    paddingVertical: 20,
    paddingHorizontal: 32,
    borderRadius: 25,
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderWidth: 2,
    borderColor: 'white',
  },
  
  secondaryButtonDisabled: {
    opacity: 0.7,
  },
  
  restoreButton: {
    paddingVertical: 12,
    alignItems: 'center',
  },
  
  // Text styles
  buttonTextPrimary: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  
  buttonTextSecondary: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  
  buttonSubtext: {
    color: 'rgba(255,255,255,0.9)',
    fontSize: 12,
    marginTop: 4,
  },
  
  restoreText: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 14,
    textDecorationLine: 'underline',
  },
});