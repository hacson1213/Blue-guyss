import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function App() {
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        let res = await fetch("https://YOUR_BACKEND_URL/predict");
        let data = await res.json();
        setPrediction(data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchPrediction();
    const interval = setInterval(fetchPrediction, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Blue Guyss Prediction</Text>
      {prediction ? (
        <>
          <Text style={styles.pred}>{prediction.next}</Text>
          <Text style={styles.money}>
            Invested: {prediction.invested} | Payout: {prediction.payout}
          </Text>
        </>
      ) : (
        <Text>Loading...</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 22, fontWeight: 'bold', color: 'blue' },
  pred: { fontSize: 40, marginTop: 10 },
  money: { fontSize: 16, marginTop: 5, color: 'gray' }
});
