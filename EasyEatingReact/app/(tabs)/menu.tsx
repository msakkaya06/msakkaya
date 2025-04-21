import { View, Text, Button } from "react-native";
import { useRouter } from "expo-router";

export default function MenuScreen() {
  const router = useRouter();

  return (
    <View>
      <Text>Menü Sayfası</Text>
      <Button title="Siparişe Git" onPress={() => router.push("/tabs/orders")} />
    </View>
  );
}
