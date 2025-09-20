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
      'es': 'Lugares Espirituales',
      'de': 'Spirituelle Orte',
    },
    'adventure_spots': {
      'en': 'Adventure Spots',
      'fr': 'Spots d\'Aventure',
      'ta': 'சாகசிக இடங்கள்',
      'hi': 'साहसिक स्थान',
      'es': 'Lugares de Aventura',
      'de': 'Abenteuer-Spots',
    },
    'current_crowd': {
      'en': 'Current crowd level',
      'fr': 'Niveau de foule actuel',
      'ta': 'தற்போதைய கூட்ட அளவு',
      'hi': 'वर्तमान भीड़ का स्तर',
      'es': 'Nivel de multitud actual',
      'de': 'Aktuelle Menschenmenge',
    },
    'best_time': {
      'en': 'Best time to visit',
      'fr': 'Meilleur moment pour visiter',
      'ta': 'பார்வையிட சிறந்த நேரம்',
      'hi': 'यात्रा का सबसे अच्छा समय',
      'es': 'Mejor momento para visitar',
      'de': 'Beste Besuchszeit',
    },
  };

  static String translate(String key, String languageCode) {
    return _translations[key]?[languageCode] ?? _translations[key]?['en'] ?? key;
  }

  static String getLanguageCode(String language) {
    Map<String, String> languageCodes = {
      'English': 'en',
      'French': 'fr',
      'Tamil': 'ta',
      'Hindi': 'hi',
      'Spanish': 'es',
      'German': 'de',
    };
    return languageCodes[language] ?? 'en';
  }
}

// services/itinerary_service.dart
class ItineraryService {
  static Map<String, dynamic> generateItinerary({
    required int days,
    required List<String> interests,
    required String budget,
    String? startLocation,
  }) {
    Map<String, dynamic> itinerary = {
      'days': [],
      'total_estimated_cost': 0,
      'transportation_tips': [],
      'weather_considerations': [],
    };

    for (int day = 1; day <= days; day++) {
      Map<String, dynamic> dayPlan = {
        'day': day,
        'theme': _getDayTheme(day, interests),
        'activities': _getActivitiesForDay(day, interests),
        'meals': _getMealRecommendations(),
        'transportation': _getTransportationForDay(day),
        'estimated_cost': _calculateDayCost(day, budget),
        'crowd_predictions': _getCrowdPredictions(day),
      };
      itinerary['days'].add(dayPlan);
    }

    itinerary['total_estimated_cost'] = _calculateTotalCost(days, budget);
    itinerary['transportation_tips'] = _getTransportationTips();
    itinerary['weather_considerations'] = _getWeatherConsiderations();

    return itinerary;
  }

  static String _getDayTheme(int day, List<String> interests) {
    List<String> themes = [];
    if (interests.contains('devotional')) themes.add('Spiritual Journey');
    if (interests.contains('adventure')) themes.add('Adventure & Nature');
    if (interests.contains('culture')) themes.add('Cultural Exploration');
    if (interests.contains('food')) themes.add('Culinary Experience');
    
    if (themes.isEmpty) themes = ['Cultural Exploration', 'Adventure & Nature', 'Spiritual Journey'];
    
    return themes[(day - 1) % themes.length];
  }

  static List<Map<String, dynamic>> _getActivitiesForDay(int day, List<String> interests) {
    Map<int, List<Map<String, dynamic>>> dayActivities = {
      1: [
        {
          'time': '08:00',
          'activity': 'Sri Aurobindo Ashram Visit',
          'duration': '2 hours',
          'location': 'White Town',
          'type': 'devotional',
        },
        {
          'time': '11:00',
          'activity': 'French Quarter Walking Tour',
          'duration': '3 hours',
          'location': 'French Quarter',
          'type': 'culture',
        },
        {
          'time': '17:00',
          'activity': 'Promenade Beach Sunset',
          'duration': '2 hours',
          'location': 'Promenade Beach',
          'type': 'relaxation',
        },
      ],
      2: [
        {
          'time': '07:00',
          'activity': 'Paradise Beach Trip',
          'duration': '4 hours',
          'location': 'Chunnambar',
          'type': 'adventure',
        },
        {
          'time': '14:00',
          'activity': 'Auroville Exploration',
          'duration': '3 hours',
          'location': 'Auroville',
          'type': 'spiritual',
        },
        {
          'time': '19:00',
          'activity': 'Local Market Visit',
          'duration': '2 hours',
          'location': 'Mission Street',
          'type': 'culture',
        },
      ],
      3: [
        {
          'time': '09:00',
          'activity': 'Scuba Diving Experience',
          'duration': '3 hours',
          'location': 'Auroville Beach',
          'type': 'adventure',
        },
        {
          'time': '15:00',
          'activity': 'Cathedral Visit',
          'duration': '1 hour',
          'location': 'Mission Street',
          'type': 'devotional',
        },
        {
          'time': '21:00',
          'activity': 'Le Club Nightlife',
          'duration': '3 hours',
          'location': 'Promenade Beach',
          'type': 'party',
        },
      ],
    };

    return dayActivities[day] ?? dayActivities[1]!;
  }

  static List<Map<String, dynamic>> _getMealRecommendations() {
    return [
      {
        'meal': 'Breakfast',
        'recommendation': 'Baker Street Cafe',
        'cuisine': 'French-Indian Fusion',
        'price_range': '₹200-400',
      },
      {
        'meal': 'Lunch',
        'recommendation': 'Surguru Restaurant',
        'cuisine': 'South Indian',
        'price_range': '₹150-300',
      },
      {
        'meal': 'Dinner',
        'recommendation': 'Villa Shanti',
        'cuisine': 'Continental',
        'price_range': '₹800-1500',
      },
    ];
  }

  static Map<String, dynamic> _getTransportationForDay(int day) {
    return {
      'recommended': 'Bike Rental',
      'cost': '₹300/day',
      'alternatives': ['Auto Rickshaw', 'Taxi', 'Walking'],
      'tips': 'Book bike early morning for best rates',
    };
  }

  static int _calculateDayCost(int day, String budget) {
    Map<String, int> budgetRanges = {
      'budget': 1500,
      'moderate': 2500,
      'luxury': 4000,
    };
    return budgetRanges[budget] ?? 2500;
  }

  static int _calculateTotalCost(int days, String budget) {
    return _calculateDayCost(1, budget) * days;
  }

  static List<String> _getTransportationTips() {
    return [
      'Rent a bike for maximum flexibility',
      'Avoid peak hours (8-10 AM, 5-7 PM) for better traffic',
      'Keep your documents handy',
      'Wear helmet at all times',
      'Use GPS navigation for unfamiliar routes',
    ];
  }

  static List<String> _getWeatherConsiderations() {
    return [
      'Carry sunscreen and hat for daytime activities',
      'Keep light jacket for evening beach visits',
      'Monsoon season (June-September): Carry umbrella',
      'Best visiting months: October to March',
    ];
  }

  static Map<String, dynamic> _getCrowdPredictions(int day) {
    return {
      'morning': 'Low to Moderate',
      'afternoon': 'Moderate to High',
      'evening': 'High (especially beaches)',
      'night': 'Low to Moderate',
    };
  }
}

// services/recommendation_engine.dart
class RecommendationEngine {
  static List<Map<String, dynamic>> getPersonalizedRecommendations({
    required Map<String, dynamic> userPreferences,
    required String currentLocation,
    required String timeOfDay,
  }) {
    List<Map<String, dynamic>> recommendations = [];
    
    // Sample recommendation logic
    if (userPreferences['interests']?.contains('adventure') == true) {
      recommendations.addAll(_getAdventureRecommendations(timeOfDay));
    }
    
    if (userPreferences['interests']?.contains('devotional') == true) {
      recommendations.addAll(_getDevotionalRecommendations(timeOfDay));
    }
    
    if (userPreferences['budget'] == 'budget') {
      recommendations = recommendations.where((rec) => 
        rec['cost_level'] == 'low' || rec['cost_level'] == 'moderate'
      ).toList();
    }
    
    // Sort by relevance score
    recommendations.sort((a, b) => 
      (b['relevance_score'] as double).compareTo(a['relevance_score'] as double)
    );
    
    return recommendations.take(5).toList();
  }

  static List<Map<String, dynamic>> _getAdventureRecommendations(String timeOfDay) {
    if (timeOfDay == 'morning') {
      return [
        {
          'name': 'Paradise Beach Adventure',
          'type': 'adventure',
          'relevance_score': 0.9,
          'cost_level': 'moderate',
          'description': 'Boat ride and water sports',
        },
        {
          'name': 'Cycling Tour',
          'type': 'adventure',
          'relevance_score': 0.8,
          'cost_level': 'low',
          'description': 'Explore French Quarter on bike',
        },
      ];
    } else if (timeOfDay == 'afternoon') {
      return [
        {
          'name': 'Scuba Diving',
          'type': 'adventure',
          'relevance_score': 0.9,
          'cost_level': 'high',
          'description': 'Underwater exploration',
        },
      ];
    }
    return [];
  }

  static List<Map<String, dynamic>> _getDevotionalRecommendations(String timeOfDay) {
    if (timeOfDay == 'morning') {
      return [
        {
          'name': 'Sri Aurobindo Ashram',
          'type': 'devotional',
          'relevance_score': 0.95,
          'cost_level': 'low',
          'description': 'Morning meditation session',
        },
        {
          'name': 'Manakula Vinayagar Temple',
          'type': 'devotional',
          'relevance_score': 0.8,
          'cost_level': 'low',
          'description': 'Ancient Ganesha temple',
        },
      ];
    }
    return [];
  }

  static Map<String, dynamic> optimizeRoute(List<String> destinations) {
    // Simple route optimization (in production, use Google Maps API)
    return {
      'optimized_order': destinations,
      'total_distance': '15 km',
      'estimated_time': '2 hours',
      'fuel_cost': '₹150',
      'traffic_condition': 'moderate',
    };
  }
}

// models/user_preference.dart
class UserPreference {
  final String userId;
  final List<String> interests;
  final String budgetLevel;
  final String preferredLanguage;
  final Map<String, int> visitHistory;
  final List<String> favoriteSpots;
  final DateTime lastUpdated;

  UserPreference({
    required this.userId,
    required this.interests,
    required this.budgetLevel,
    required this.preferredLanguage,
    required this.visitHistory,
    required this.favoriteSpots,
    required this.lastUpdated,
  });

  Map<String, dynamic> toJson() {
    return {
      'userId': userId,
      'interests': interests,
      'budgetLevel': budgetLevel,
      'preferredLanguage': preferredLanguage,
      'visitHistory': visitHistory,
      'favoriteSpots': favoriteSpots,
      'lastUpdated': lastUpdated.toIso8601String(),
    };
  }

  static UserPreference fromJson(Map<String, dynamic> json) {
    return UserPreference(
      userId: json['userId'],
      interests: List<String>.from(json['interests'] ?? []),
      budgetLevel: json['budgetLevel'] ?? 'moderate',
      preferredLanguage: json['preferredLanguage'] ?? 'English',
      visitHistory: Map<String, int>.from(json['visitHistory'] ?? {}),
      favoriteSpots: List<String>.from(json['favoriteSpots'] ?? []),
      lastUpdated: DateTime.parse(json['lastUpdated'] ?? DateTime.now().toIso8601String()),
    );
  }
}
