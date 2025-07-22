# Screens Directory Structure

This directory contains organized, modular screens for better maintainability and scalability.

**Note:** The `screens/` directory is located outside of `app/` to prevent Expo Router from creating unwanted routes.

## Structure

```
screens/
├── README.md
├── index.ts                    # Main export file for all screens
└── paywall/
    ├── index.ts               # Paywall screen exports
    ├── PaywallScreen.tsx      # Main paywall component
    ├── components/            # Paywall-specific components
    │   ├── index.ts
    │   ├── BackgroundAnimation.tsx
    │   ├── PaywallHeader.tsx
    │   ├── PurchaseButtons.tsx
    │   └── WordCarousel.tsx
    └── styles/
        └── paywall.styles.ts  # Centralized styles
```

## Benefits

### 1. **Separation of Concerns**
- Each component has a single responsibility
- Styles are separated from logic
- State management is centralized in Zustand stores

### 2. **Scalability**
- Easy to add new screens (chat, profile, settings, etc.)
- Components are reusable across screens
- Clear file organization prevents bloat

### 3. **Maintainability** 
- Small, focused files are easier to debug
- Styles are centralized and consistent
- State logic is separate from UI components

## Adding New Screens

To add a new screen:

1. Create a new directory: `screens/new-screen/`
2. Add the main component: `NewScreen.tsx`
3. Create components directory: `components/`
4. Create styles file: `styles/new-screen.styles.ts`
5. Add exports in `index.ts` files
6. Create a Zustand store if needed in `stores/`

## State Management

- Use Zustand stores for complex state (see `stores/paywall.store.ts`)
- Keep simple local state in components with `useState`
- Store files should be named `[screen-name].store.ts`

## Styling

- Use StyleSheet.create for performance
- Group related styles logically
- Use consistent naming conventions
- Consider extracting common styles to a shared styles file