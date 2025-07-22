# Development Options Guide

## Expo Go (For Development)

**✅ Current Setup** - You can use Expo Go for most development work:

```bash
npx expo start
```

The IAP functionality will use the mock implementation we created, so you can test the purchase flow without real payments.

## Development Build (For IAP Testing)

Only needed when you want to test **real** in-app purchases on device. Since your app uses `react-native-iap` (which requires native code), you'll need a development build for production IAP testing.

## Option 1: EAS Build (Recommended)

### Step 1: Initialize EAS Project
```bash
cd mobile_app/musiclands-ai
eas init
# Answer "y" to create a project
```

### Step 2: Build Development Client
```bash
# For iOS (if you have an iPhone)
eas build --profile development --platform ios

# For Android (if you have an Android device)
eas build --profile development --platform android
```

### Step 3: Install on Device
1. Once the build completes, you'll get a download link
2. Install the development build on your device
3. Open the installed app
4. It will show a screen asking for the development server URL

### Step 4: Connect to Development Server
```bash
npx expo start --dev-client
```
The app will automatically connect and reload when you make changes.

## Option 2: Local Development Build (Advanced)

If you prefer to build locally and have Xcode/Android Studio set up:

### Step 1: Prebuild
```bash
npx expo prebuild --platform ios
# or
npx expo prebuild --platform android
```

### Step 2: Build with Native Tools
```bash
# iOS (requires Xcode)
npx expo run:ios

# Android (requires Android Studio)
npx expo run:android
```

## Configuration Files Already Created

✅ `eas.json` - EAS build configuration
✅ `app.json` - Updated with bundle identifiers
✅ `expo-dev-client` - Installed for development builds

## Troubleshooting

### If you get "No development build installed" error:
This means you need to complete the build process above. The app must be built with the development client to work with `react-native-iap`.

### If the build fails:
1. Make sure you're logged into EAS: `eas whoami`
2. Check your EAS usage limits on expo.dev
3. Verify your app.json bundle identifier is unique

### If you don't have a device:
You can use the iOS Simulator or Android Emulator, but IAP testing will be limited to the mock mode we set up.

## Next Steps

1. Run `eas init` to create the project
2. Run `eas build --profile development --platform ios` (or android)
3. Install the built app on your device
4. Run `npx expo start --dev-client` to start development

The development build includes all the native dependencies (like react-native-iap) and will work with the purchase flow we implemented!