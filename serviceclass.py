// services/ai_service.dart
import 'dart:convert';
import 'dart:math';

class AIService {
  static const Map<String, List<String>> _intentKeywords = {
    'devotional': ['temple', 'spiritual', 'prayer', 'ashram', 'devotional', 'meditation', 'peace'],
    'adventure': ['adventure', 'beach', 'diving', 'water sports', 'thrilling', 'exciting', 'outdoor'],
    'party': ['party', 'nightlife', 'club', 'bar', 'music', 'dance', 'drinks'],
    'transport': ['bike', 'rental', 'transport', 'vehicle', 'scooter', 'travel'],
    'events': ['event', 'festival', 'celebration', 'culture', 'show', 'performance'],
    'food': ['food', 'restaurant', 'eat', 'cuisine', 'dining', 'meal', 'hungry'],
    'accommodation': ['hotel', 'stay', 'accommodation', 'room', 'lodge', 'guesthouse'],
    'budget': ['budget', 'cheap', 'affordable', 'cost', 'price', 'money', 'expense'],
    'itinerary': ['plan', 'itinerary', 'schedule', 'route', 'trip', 'visit', 'tour'],
  };

  static String classifyIntent(String message) {
    String lowerMessage = message.toLowerCase();
    Map<String, int> intentScores = {};

    for (String intent in _intentKeywords.keys) {
      int score = 0;
      for (String keyword in _intentKeywords[intent]!) {
        if (lowerMessage.contains(keyword)) {
          score++;
        }
      }
      if (score > 0) {
        intentScores[intent] = score;
      }
    }

    if (intentScores.isEmpty) return 'general';
    
    return intentScores.entries
        .reduce((a, b) => a.value > b.value ? a : b)
        .key;
  }

  static double calculateSentiment(String message) {
    List<String> positiveWords = ['good', 'great', 'amazing', 'love', 'beautiful', 'wonderful', 'excellent'];
    List<String> negativeWords = ['bad', 'terrible', 'awful', 'hate', 'horrible', 'disappointing'];
    
    String lowerMessage = message.toLowerCase();
    double sentiment = 0.0;
    
    for (String word in positiveWords) {
      if (lowerMessage.contains(word)) sentiment += 0.1;
    }
    
    for (String word in negativeWords) {
      if (lowerMessage.contains(word)) sentiment -= 0.1;
    }
    
    return sentiment.clamp(-1.0, 1.0);
  }
}

// services/location_service.dart
class LocationService {
  static const Map<String, Map<String, double>> _pondyLocations = {
    'Sri Aurobindo Ashram': {'lat': 11.9416, 'lng': 79.8083},
    'French Quarter': {'lat': 11.9344, 'lng': 79.8309},
    'Paradise Beach': {'lat': 12.0167, 'lng': 79.8667},
    'Auroville': {'lat': 12.0051, 'lng': 79.8095},
    'Promenade Beach': {'lat': 11.9270, 'lng': 79.8368},
  };

  static double calculateDistance(String location1, String location2) {
    if (!_pondyLocations.containsKey(location1) || !_pondyLocations.containsKey(location2)) {
      return 0.0;
    }
    
    var loc1 = _pondyLocations[location1]!;
    var loc2 = _pondyLocations[location2]!;
    
    // Simplified distance calculation (Haversine formula would be more accurate)
    double deltaLat = (loc1['lat']! - loc2['lat']!);
    double deltaLng = (loc1['lng']! - loc2['lng']!);
    
    return sqrt(deltaLat * deltaLat + deltaLng * deltaLng) * 111; // Approximate km
  }

  static String getTrafficCondition(String location) {
    // Simulate real-time traffic data
    Random random = Random();
    List<String> conditions = ['light', 'moderate', 'heavy'];
    return conditions[random.nextInt(conditions.length)];
  }

  static String getCrowdDensity(String location) {
    // Simulate crowd density based on location and time
    DateTime now = DateTime.now();
    int hour = now.hour;
    
    if (location.contains('Beach') && (hour >= 17 && hour <= 20)) {
      return 'high'; // Evening beach crowds
    } else if (location.contains('Ashram') && (hour >= 6 && hour <= 10)) {
      return 'moderate'; // Morning meditation
    } else {
      return 'low';
    }
  }
}

// services/translation_service.dart
class TranslationService {
  static const Map<String, Map<String, String>> _translations = {
    'welcome': {
      'en': 'Welcome to Pondicherry!',
      'fr': 'Bienvenue à Pondichéry!',
      'ta': 'பாண்டிச்சேரிக்கு வரவேற்கிறோம்!',
      'hi': 'पांडिचेरी में आपका स्वागत है!',
      'es': '¡Bienvenido a Pondicherry!',
      'de': 'Willkommen in Pondicherry!',
    },
    'how_can_help': {
      'en': 'How can I help you explore?',
      'fr': 'Comment puis-je vous aider à explorer?',
      'ta': 'நான் எப்படி உங்களுக்கு உதவ முடியும்?',
      'hi': 'मैं आपकी कैसे मदद कर सकता हूं?',
      'es': '¿Cómo puedo ayudarte a explorar?',
      'de': 'Wie kann ich Ihnen beim Erkunden helfen?',
    },
    'spiritual_places': {
      'en': 'Spiritual Places',
      'fr': 'Lieux Spirituels',
      'ta': 'ஆன்மீக இடங்கள்',
      'hi': 'आध्यात्मिक स्थान',
      'es': '
