# In-App Purchase Setup Guide

## Product Configuration

You need to create the following products in your App Store Connect (iOS) and Google Play Console (Android):

### Product IDs
- `premium_3day` - 3-day premium access for $4.99
- `premium_1day` - 1-day premium access for $1.99

## iOS App Store Connect Setup

1. Go to App Store Connect → Your App → Features → In-App Purchases
2. Create two new **Non-Consumable** products:

### Premium 3-Day Access
- **Product ID:** `premium_3day`
- **Reference Name:** Premium 3-Day Access
- **Price Tier:** $4.99 USD (Tier 5)
- **Display Name:** 3-Day Premium Access
- **Description:** Get premium access to Music Land AI for 3 days

### Premium 1-Day Access
- **Product ID:** `premium_1day`
- **Reference Name:** Premium 1-Day Access  
- **Price Tier:** $1.99 USD (Tier 2)
- **Display Name:** 1-Day Premium Access
- **Description:** Get premium access to Music Land AI for 1 day

## Google Play Console Setup

1. Go to Google Play Console → Your App → Monetize → Products → In-app products
2. Create two new products:

### Premium 3-Day Access
- **Product ID:** `premium_3day`
- **Name:** 3-Day Premium Access
- **Description:** Get premium access to Music Land AI for 3 days
- **Price:** $4.99 USD

### Premium 1-Day Access
- **Product ID:** `premium_1day`
- **Name:** 1-Day Premium Access
- **Description:** Get premium access to Music Land AI for 1 day
- **Price:** $1.99 USD

## Testing

### iOS Testing
1. Create sandbox test users in App Store Connect
2. Sign out of App Store on device
3. Run the app and attempt purchases
4. Sign in with sandbox test user when prompted

### Android Testing
1. Create test accounts in Google Play Console
2. Upload app to Internal Testing track
3. Install from Play Store and test purchases

## Important Notes

- Products must be approved before they work in production
- iOS products need to be submitted for review
- Android products are approved automatically but may take time to propagate
- Test thoroughly in sandbox/test environments before releasing
- The IAP service handles purchase validation and expiration automatically