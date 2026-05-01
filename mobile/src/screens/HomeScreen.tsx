import { StyleSheet, Text, View } from "react-native";

// Pantalla de inicio para mostrar resumen de emergencias y actividad reciente.
export function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Resumen de emergencias</Text>
      <Text>En esta sección se visualizarán reportes activos y estados recientes.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    marginBottom: 8,
  },
});

