import { useState } from "react";
import { SafeAreaProvider } from "react-native-safe-area-context";

import { EmergencyFormScreen } from "../src/screens/EmergencyFormScreen";
import { EmergencyListScreen } from "../src/screens/EmergencyListScreen";
import { HomeScreen } from "../src/screens/HomeScreen";
import { LoginScreen } from "../src/screens/LoginScreen";

type ScreenRoute = "login" | "home" | "form" | "list";

// Flujo inicial simulado. Expo Router se mantiene como punto de entrada.
export default function Index() {
  const [screen, setScreen] = useState<ScreenRoute>("login");

  return (
    <SafeAreaProvider>
      {screen === "login" ? <LoginScreen onLoginSuccess={() => setScreen("home")} /> : null}
      {screen === "home" ? (
        <HomeScreen
          onLogout={() => setScreen("login")}
          onRegisterEmergency={() => setScreen("form")}
          onViewEmergencies={() => setScreen("list")}
        />
      ) : null}
      {screen === "form" ? <EmergencyFormScreen onBack={() => setScreen("home")} /> : null}
      {screen === "list" ? (
        <EmergencyListScreen onBack={() => setScreen("home")} onRegisterEmergency={() => setScreen("form")} />
      ) : null}
    </SafeAreaProvider>
  );
}
