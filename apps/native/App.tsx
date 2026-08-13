import { useState } from "react";
import { Pressable, SafeAreaView, StyleSheet, Text, View } from "react-native";
import { colors, spacing } from "@barclimb/design-tokens";

const destinations = ["Home", "Practice", "Simulate", "Progress"] as const;

export default function App() {
  const [active, setActive] = useState<(typeof destinations)[number]>("Home");
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.content}>
        <Text style={styles.brand}>BarClimb</Text>
        <Text style={styles.eyebrow}>Foundation build</Text>
        <Text style={styles.title}>{active} shell</Text>
        <Text>
          No learner features or native parity claims are implemented in M1.1.
        </Text>
      </View>
      <View accessibilityRole="tablist" style={styles.tabs}>
        {destinations.map((destination) => (
          <Pressable
            accessibilityRole="tab"
            accessibilityState={{ selected: active === destination }}
            key={destination}
            onPress={() => setActive(destination)}
          >
            <Text
              style={active === destination ? styles.activeTab : styles.tab}
            >
              {destination}
            </Text>
          </Pressable>
        ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: colors.background },
  content: { flex: 1, padding: spacing[6], justifyContent: "center" },
  brand: { fontSize: 18, fontWeight: "700", color: colors.text },
  eyebrow: { marginTop: spacing[8], color: colors.accent, fontWeight: "700" },
  title: {
    fontSize: 30,
    fontWeight: "700",
    color: colors.text,
    marginVertical: spacing[3],
  },
  tabs: {
    flexDirection: "row",
    justifyContent: "space-around",
    padding: spacing[4],
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  tab: { color: colors.muted },
  activeTab: { color: colors.accent, fontWeight: "700" },
});
