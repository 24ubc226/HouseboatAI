import pandas as pd

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from .models import ProfessionalHouseboatDataset500Rows


# =========================================================
# COMMON AI FEATURE COLUMNS
# =========================================================

FEATURE_COLUMNS = [
    "priceinr",
    "rating",
    "capacity",
    "bedrooms",
    "bookingcount",
    "reviewcount",
    "latitude",
    "longitude",
]


# =========================================================
# PREPARE FEATURES
# =========================================================

def prepare_features(df):
    """
    Converts AI feature columns into numeric values
    and handles missing values.
    """

    features = df[FEATURE_COLUMNS].copy()

    features = features.apply(
        pd.to_numeric,
        errors="coerce"
    )

    features = features.fillna(0)

    return features


# =========================================================
# BUILD KNN MODEL
# =========================================================

def build_knn_model(df, n_neighbors=6):
    """
    Builds the StandardScaler and KNN model.
    """

    features = prepare_features(df)

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        features
    )

    number_of_neighbors = min(
        n_neighbors,
        len(df)
    )

    model = NearestNeighbors(
        n_neighbors=number_of_neighbors,
        metric="cosine"
    )

    model.fit(
        scaled_features
    )

    return (
        model,
        scaler,
        scaled_features
    )


# =========================================================
# CALCULATE AI SCORE
# =========================================================

def calculate_ai_score(distance, boat):
    """
    Calculates the AI recommendation score.

    Score components:

    50% - KNN similarity
    30% - Rating
    20% - Popularity
    """

    # -----------------------------------------------------
    # COSINE DISTANCE → SIMILARITY
    # -----------------------------------------------------

    similarity_score = max(
        0,
        min(
            100,
            (1 - float(distance)) * 100
        )
    )


    # -----------------------------------------------------
    # RATING SCORE
    # -----------------------------------------------------

    try:

        rating_score = (
            float(boat.rating or 0)
            / 5
        ) * 100

    except (
        ValueError,
        TypeError
    ):

        rating_score = 0


    rating_score = max(
        0,
        min(
            100,
            rating_score
        )
    )


    # -----------------------------------------------------
    # POPULARITY SCORE
    # -----------------------------------------------------

    try:

        popularity_score = min(
            float(
                boat.bookingcount or 0
            ) / 100,
            1
        ) * 100

    except (
        ValueError,
        TypeError
    ):

        popularity_score = 0


    popularity_score = max(
        0,
        min(
            100,
            popularity_score
        )
    )


    # -----------------------------------------------------
    # FINAL AI SCORE
    # -----------------------------------------------------

    final_score = round(
        similarity_score * 0.50
        +
        rating_score * 0.30
        +
        popularity_score * 0.20
    )


    # Keep score between 0 and 100

    final_score = max(
        0,
        min(
            100,
            final_score
        )
    )

    return final_score


# =========================================================
# BUILD RECOMMENDATION REASONS
# =========================================================

def build_reasons(
    selected_boat,
    boat
):

    reasons = []


    # -----------------------------------------------------
    # SAME LOCATION
    # -----------------------------------------------------

    if (
        str(boat.location).lower()
        ==
        str(
            selected_boat["location"]
        ).lower()
    ):

        reasons.append(
            "📍 Same Location"
        )


    # -----------------------------------------------------
    # SIMILAR PRICE
    # -----------------------------------------------------

    try:

        price_difference = abs(
            float(
                boat.priceinr or 0
            )
            -
            float(
                selected_boat["priceinr"]
                or 0
            )
        )

        if price_difference <= 2000:

            reasons.append(
                "💰 Similar Price"
            )

    except (
        ValueError,
        TypeError
    ):

        pass


    # -----------------------------------------------------
    # HIGH RATING
    # -----------------------------------------------------

    try:

        if float(
            boat.rating or 0
        ) >= 4.5:

            reasons.append(
                "⭐ Highly Rated"
            )

    except (
        ValueError,
        TypeError
    ):

        pass


    # -----------------------------------------------------
    # LUXURY
    # -----------------------------------------------------

    if (
        str(
            boat.luxury
        ).lower()
        == "yes"
    ):

        reasons.append(
            "🏆 Luxury Boat"
        )


    # -----------------------------------------------------
    # SIMILAR CAPACITY
    # -----------------------------------------------------

    try:

        if int(
            boat.capacity or 0
        ) == int(
            selected_boat["capacity"]
            or 0
        ):

            reasons.append(
                "👥 Similar Capacity"
            )

    except (
        ValueError,
        TypeError
    ):

        pass


    # -----------------------------------------------------
    # SIMILAR BEDROOMS
    # -----------------------------------------------------

    try:

        if int(
            boat.bedrooms or 0
        ) == int(
            selected_boat["bedrooms"]
            or 0
        ):

            reasons.append(
                "🛏 Similar Bedrooms"
            )

    except (
        ValueError,
        TypeError
    ):

        pass


    # -----------------------------------------------------
    # DEFAULT REASON
    # -----------------------------------------------------

    if not reasons:

        reasons.append(
            "🤖 AI Similar Match"
        )


    return reasons


# =========================================================
# GET HOUSEBOAT RECOMMENDATIONS
# =========================================================

def get_recommendations(
    houseboat_id
):

    # -----------------------------------------------------
    # GET HOUSEBOATS
    # -----------------------------------------------------

    boats = (
        ProfessionalHouseboatDataset500Rows
        .objects
        .all()
    )

    df = pd.DataFrame(
        list(
            boats.values()
        )
    )


    if df.empty:

        return []


    # -----------------------------------------------------
    # BUILD KNN
    # -----------------------------------------------------

    model, scaler, scaled_features = (
        build_knn_model(
            df,
            n_neighbors=6
        )
    )


    # -----------------------------------------------------
    # FIND SELECTED HOUSEBOAT
    # -----------------------------------------------------

    matching_rows = df[
        df["houseboatid"]
        .astype(str)
        ==
        str(houseboat_id)
    ]


    if matching_rows.empty:

        return []


    index = matching_rows.index[0]

    position = df.index.get_loc(
        index
    )


    # -----------------------------------------------------
    # FIND SIMILAR BOATS
    # -----------------------------------------------------

    distances, indices = (
        model.kneighbors(
            [
                scaled_features[
                    position
                ]
            ]
        )
    )


    recommendations = []

    selected_boat = df.iloc[
        position
    ]


    # -----------------------------------------------------
    # PROCESS RECOMMENDATIONS
    # -----------------------------------------------------

    for i in range(
        1,
        len(indices[0])
    ):

        recommended_index = (
            indices[0][i]
        )

        recommended_id = (
            df.iloc[
                recommended_index
            ]["houseboatid"]
        )


        # -------------------------------------------------
        # GET BOAT
        # -------------------------------------------------

        try:

            boat = (
                ProfessionalHouseboatDataset500Rows
                .objects
                .get(
                    houseboatid=
                    recommended_id
                )
            )

        except (
            ProfessionalHouseboatDataset500Rows
            .DoesNotExist
        ):

            continue


        # -------------------------------------------------
        # AI SCORE
        # -------------------------------------------------

        distance = distances[0][i]

        score = calculate_ai_score(
            distance,
            boat
        )


        # -------------------------------------------------
        # REASONS
        # -------------------------------------------------

        reasons = build_reasons(
            selected_boat,
            boat
        )


        # -------------------------------------------------
        # ADD RECOMMENDATION
        # -------------------------------------------------

        recommendations.append(
            {
                "boat": boat,
                "score": score,
                "reason": reasons,
            }
        )


    # -----------------------------------------------------
    # SORT BY SCORE
    # -----------------------------------------------------

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return recommendations[:5]


# =========================================================
# PERSONALIZED AI RECOMMENDATIONS
# =========================================================

def get_personalized_recommendations(
    location=None,
    max_price=None,
    bedrooms=None,
    capacity=None,
    ac=None,
    wifi=None,
    luxury=None
):

    # =====================================================
    # GET ALL HOUSEBOATS
    # =====================================================

    boats = (
        ProfessionalHouseboatDataset500Rows
        .objects
        .all()
    )


    if not boats.exists():

        return []


    # =====================================================
    # CONVERT TO DATAFRAME
    # =====================================================

    df = pd.DataFrame(
        list(
            boats.values()
        )
    )


    if df.empty:

        return []


    # =====================================================
    # BUILD KNN MODEL
    # =====================================================

    model, scaler, scaled_features = (
        build_knn_model(
            df,
            n_neighbors=5
        )
    )


    features = prepare_features(
        df
    )


    # =====================================================
    # USER PRICE
    # =====================================================

    try:

        user_price = (
            float(max_price)
            if max_price
            else features[
                "priceinr"
            ].mean()
        )

    except (
        ValueError,
        TypeError
    ):

        user_price = features[
            "priceinr"
        ].mean()


    # =====================================================
    # USER BEDROOMS
    # =====================================================

    try:

        user_bedrooms = (
            int(bedrooms)
            if bedrooms
            else features[
                "bedrooms"
            ].mean()
        )

    except (
        ValueError,
        TypeError
    ):

        user_bedrooms = features[
            "bedrooms"
        ].mean()


    # =====================================================
    # USER CAPACITY
    # =====================================================

    try:

        user_capacity = (
            int(capacity)
            if capacity
            else features[
                "capacity"
            ].mean()
        )

    except (
        ValueError,
        TypeError
    ):

        user_capacity = features[
            "capacity"
        ].mean()


    # =====================================================
    # USER FEATURE VECTOR
    # =====================================================

    user_features = pd.DataFrame(
        [[
            user_price,

            features[
                "rating"
            ].mean(),

            user_capacity,

            user_bedrooms,

            features[
                "bookingcount"
            ].mean(),

            features[
                "reviewcount"
            ].mean(),

            features[
                "latitude"
            ].mean(),

            features[
                "longitude"
            ].mean(),
        ]],
        columns=FEATURE_COLUMNS
    )


    # =====================================================
    # SCALE USER FEATURES
    # =====================================================

    user_features_scaled = (
        scaler.transform(
            user_features
        )
    )


    # =====================================================
    # KNN SEARCH
    # =====================================================

    distances, indices = (
        model.kneighbors(
            user_features_scaled
        )
    )


    recommendations = []


    # =====================================================
    # PROCESS RESULTS
    # =====================================================

    for i in range(
        len(indices[0])
    ):

        recommended_index = (
            indices[0][i]
        )


        boat_id = (
            df.iloc[
                recommended_index
            ]["houseboatid"]
        )


        # -------------------------------------------------
        # GET BOAT
        # -------------------------------------------------

        try:

            boat = (
                ProfessionalHouseboatDataset500Rows
                .objects
                .get(
                    houseboatid=boat_id
                )
            )

        except (
            ProfessionalHouseboatDataset500Rows
            .DoesNotExist
        ):

            continue


        # =================================================
        # BASE AI SCORE
        # =================================================

        distance = distances[0][i]

        knn_score = calculate_ai_score(
            distance,
            boat
        )


        # =================================================
        # USER PREFERENCE SCORE
        # =================================================

        preference_score = 0

        matched_preferences = []


        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------

        if location:

            if (
                location.lower()
                in
                str(
                    boat.location
                ).lower()
            ):

                preference_score += 25

                matched_preferences.append(
                    "📍 Preferred Location"
                )


        # -------------------------------------------------
        # BUDGET
        # -------------------------------------------------

        try:

            boat_price = float(
                boat.priceinr or 0
            )

            if max_price:

                if boat_price <= float(
                    max_price
                ):

                    preference_score += 20

                    matched_preferences.append(
                        "💰 Within Your Budget"
                    )

                else:

                    preference_score -= 10

        except (
            ValueError,
            TypeError
        ):

            pass


        # -------------------------------------------------
        # BEDROOMS
        # -------------------------------------------------

        try:

            if bedrooms:

                if int(
                    boat.bedrooms or 0
                ) >= int(
                    bedrooms
                ):

                    preference_score += 10

                    matched_preferences.append(
                        "🛏 Suitable Bedrooms"
                    )

        except (
            ValueError,
            TypeError
        ):

            pass


        # -------------------------------------------------
        # CAPACITY
        # -------------------------------------------------

        try:

            if capacity:

                if int(
                    boat.capacity or 0
                ) >= int(
                    capacity
                ):

                    preference_score += 10

                    matched_preferences.append(
                        "👥 Suitable Capacity"
                    )

        except (
            ValueError,
            TypeError
        ):

            pass


        # -------------------------------------------------
        # AC
        # -------------------------------------------------

        if ac:

            if (
                str(
                    boat.ac
                ).lower()
                ==
                str(ac).lower()
            ):

                preference_score += 10

                matched_preferences.append(
                    "❄️ AC Preference Matched"
                )


        # -------------------------------------------------
        # WIFI
        # -------------------------------------------------

        if wifi:

            if (
                str(
                    boat.wifi
                ).lower()
                ==
                str(wifi).lower()
            ):

                preference_score += 10

                matched_preferences.append(
                    "📶 WiFi Preference Matched"
                )


        # -------------------------------------------------
        # LUXURY
        # -------------------------------------------------

        if luxury:

            if (
                str(
                    boat.luxury
                ).lower()
                ==
                str(luxury).lower()
            ):

                preference_score += 10

                matched_preferences.append(
                    "🏆 Luxury Preference Matched"
                )


        # -------------------------------------------------
        # HIGH RATING
        # -------------------------------------------------

        try:

            if float(
                boat.rating or 0
            ) >= 4.5:

                preference_score += 5

                matched_preferences.append(
                    "⭐ Highly Rated"
                )

        except (
            ValueError,
            TypeError
        ):

            pass


        # =================================================
        # COMBINE AI + USER PREFERENCES
        # =================================================

        final_score = round(
            (knn_score * 0.40)
            +
            (preference_score * 0.60)
        )


        # Keep score between 0 and 100

        final_score = max(
            0,
            min(
                100,
                final_score
            )
        )


        # =================================================
        # DEFAULT REASON
        # =================================================

        if not matched_preferences:

            matched_preferences.append(
                "🤖 Similar to your selected preferences"
            )


        # =================================================
        # ADD RESULT
        # =================================================

        recommendations.append(
            {
                "boat": boat,
                "score": final_score,
                "reason": matched_preferences,
            }
        )


    # =====================================================
    # SORT RESULTS
    # =====================================================

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # =====================================================
    # RETURN TOP 5
    # =====================================================

    return recommendations[:5]
