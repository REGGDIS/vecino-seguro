import { useState } from "react";
import { SafeAreaProvider } from "react-native-safe-area-context";

import { EmergencyFormScreen } from "../src/screens/EmergencyFormScreen";
import { EmergencyListScreen } from "../src/screens/EmergencyListScreen";
import { HomeScreen } from "../src/screens/HomeScreen";
import { LoginScreen } from "../src/screens/LoginScreen";
import type { AuthenticatedUser } from "../src/types/auth";

type ScreenRoute = "login" | "home" | "form" | "list";

// Expo Router se mantiene como punto de entrada del flujo simple de la app.
export default function Index() {
  const [screen, setScreen] = useState<ScreenRoute>("login");
  const [authenticatedUser, setAuthenticatedUser] = useState<AuthenticatedUser | null>(null);

  return (
    <SafeAreaProvider>
      {screen === "login" ? (
        <LoginScreen
          onLoginSuccess={(user) => {
            setAuthenticatedUser(user);
            setScreen("home");
          }}
        />
      ) : null}
      {screen === "home" ? (
        <HomeScreen
          onLogout={() => {
            setAuthenticatedUser(null);
            setScreen("login");
          }}
          onRegisterEmergency={() => setScreen("form")}
          onViewEmergencies={() => setScreen("list")}
          user={authenticatedUser}
        />
      ) : null}
      {screen === "form" ? <EmergencyFormScreen onBack={() => setScreen("home")} /> : null}
      {screen === "list" ? (
        <EmergencyListScreen onBack={() => setScreen("home")} onRegisterEmergency={() => setScreen("form")} />
      ) : null}
    </SafeAreaProvider>
  );
}
