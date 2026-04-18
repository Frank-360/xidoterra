def safe_lower(value):
    return value.lower() if isinstance(value, str) else ""


# 🌱 BASE NUTRIENT PREDICTION
def predict_nutrients(crop, soil_color, previous_yield, fertilizer_used):

    crop = safe_lower(crop)
    soil_color = safe_lower(soil_color)
    previous_yield = safe_lower(previous_yield)
    fertilizer_used = safe_lower(fertilizer_used)

    nutrients = {
        "nitrogen": "medium",
        "phosphorus": "medium",
        "potassium": "medium"
    }

    if soil_color in ["light", "sandy"]:
        nutrients["potassium"] = "low"

    elif soil_color in ["dark", "black"]:
        nutrients["nitrogen"] = "high"

    if previous_yield == "low":
        nutrients["phosphorus"] = "low"

    elif previous_yield == "high":
        nutrients["potassium"] = "low"

    if fertilizer_used == "organic":
        nutrients["nitrogen"] = "high"

    elif fertilizer_used == "chemical":
        nutrients["phosphorus"] = "high"

    return nutrients


# 🌍 LOCATION INTELLIGENCE
def adjust_by_location(nutrients, location):

    location = safe_lower(location)
    insights = []

    north_states = [
        "kano", "kaduna", "katsina", "sokoto", "borno", "yobe",
        "zamfara", "jigawa", "bauchi", "gombe", "adamawa", "taraba"
    ]

    south_states = [
        "lagos", "ogun", "oyo", "osun", "ondo", "ekiti",
        "rivers", "delta", "akwa ibom", "bayelsa", "cross river", "edo"
    ]

    if any(state in location for state in north_states):
        insights.append("Dry region detected → soil may lose nutrients quickly")

        if nutrients["nitrogen"] == "high":
            nutrients["nitrogen"] = "medium"

        if nutrients["potassium"] == "high":
            nutrients["potassium"] = "medium"

    elif any(state in location for state in south_states):
        insights.append("High rainfall region → nutrients may be washed away (leaching)")

        if nutrients["nitrogen"] == "high":
            nutrients["nitrogen"] = "medium"

        if nutrients["phosphorus"] == "high":
            nutrients["phosphorus"] = "medium"

    else:
        insights.append("No strong regional effect detected")

    return nutrients, insights


# 🌱 CROP INTELLIGENCE
def adjust_by_crop(nutrients, crop):

    crop = safe_lower(crop)
    crop_insights = []

    if "maize" in crop or "corn" in crop:
        crop_insights.append("Maize requires high nitrogen for optimal growth")

        if nutrients["nitrogen"] == "low":
            nutrients["nitrogen"] = "medium"

    elif "rice" in crop:
        crop_insights.append("Rice thrives in nitrogen-rich and water conditions")

        if nutrients["nitrogen"] == "low":
            nutrients["nitrogen"] = "medium"

    elif "cassava" in crop:
        nutrients["potassium"] = "high"
        crop_insights.append("Cassava benefits from high potassium")

    elif "beans" in crop:
        nutrients["nitrogen"] = "medium"
        crop_insights.append("Beans fix nitrogen naturally")

    else:
        crop_insights.append("No specific crop intelligence applied")

    return nutrients, crop_insights


# 💡 RECOMMENDATIONS
def generate_recommendation(nutrients, insights):

    recommendations = []

    high_rainfall = any("rainfall" in ins.lower() for ins in insights)
    dry_region = any("dry region" in ins.lower() for ins in insights)

    if nutrients["nitrogen"] == "low":
        if high_rainfall:
            recommendations.append("Apply Nitrogen fertilizer AFTER rainfall")
        elif dry_region:
            recommendations.append("Apply Nitrogen fertilizer with irrigation support")
        else:
            recommendations.append("Apply Nitrogen fertilizer (Urea or NPK)")

    if nutrients["phosphorus"] == "low":
        if high_rainfall:
            recommendations.append("Apply Phosphorus in split doses")
        else:
            recommendations.append("Apply Phosphorus fertilizer (SSP or NPK)")

    if nutrients["potassium"] == "low":
        if high_rainfall:
            recommendations.append("Apply Potassium carefully due to leaching")
        else:
            recommendations.append("Apply Potassium fertilizer (MOP)")

    if nutrients["nitrogen"] == "high":
        recommendations.append("Reduce nitrogen application to avoid crop damage")

    if len(recommendations) == 0:
        recommendations.append("Soil is balanced. Maintain good practices")

    return recommendations


# 🌟 SMART SUMMARY
def generate_summary(nutrients, crop, insights):

    crop = safe_lower(crop)
    summary = []

    if all(v == "medium" for v in nutrients.values()):
        summary.append("Soil is moderately fertile")
    elif any(v == "low" for v in nutrients.values()):
        summary.append("Soil has nutrient deficiencies")
    else:
        summary.append("Soil is in good condition")

    if "maize" in crop:
        if nutrients["nitrogen"] != "high":
            summary.append("nitrogen is not sufficient for maize")

    elif "cassava" in crop:
        summary.append("potassium is important for cassava growth")

    elif "rice" in crop:
        summary.append("rice requires strong nitrogen support")

    if any("rainfall" in ins.lower() for ins in insights):
        summary.append("high rainfall may reduce nutrient availability")

    elif any("dry region" in ins.lower() for ins in insights):
        summary.append("dry conditions may affect nutrient uptake")

    return ". ".join(summary) + "."


# 🧪 FERTILIZER PLAN
def generate_fertilizer_plan(nutrients, crop, insights):

    crop = safe_lower(crop)
    plan = []

    high_rainfall = any("rainfall" in ins.lower() for ins in insights)

    if "maize" in crop or "corn" in crop:

        if nutrients["nitrogen"] in ["low", "medium"]:
            qty = "60 kg/ha" if nutrients["nitrogen"] == "low" else "40 kg/ha"

            if high_rainfall:
                plan.append(f"Apply {qty} of NPK 15-15-15 AFTER rainfall (split into 2 applications)")
            else:
                plan.append(f"Apply {qty} of NPK 15-15-15")

        if nutrients["phosphorus"] == "low":
            plan.append("Apply 30 kg/ha of SSP for phosphorus support")

    elif "cassava" in crop:

        if nutrients["potassium"] in ["low", "medium"]:
            plan.append("Apply 50 kg/ha of MOP (Potassium fertilizer)")

    elif "rice" in crop:

        plan.append("Apply 40–60 kg/ha of Nitrogen fertilizer in 2 splits")

    else:

        if nutrients["nitrogen"] == "low":
            plan.append("Apply 40 kg/ha of Nitrogen fertilizer")

        if nutrients["phosphorus"] == "low":
            plan.append("Apply 30 kg/ha of Phosphorus fertilizer")

        if nutrients["potassium"] == "low":
            plan.append("Apply 30 kg/ha of Potassium fertilizer")

        if len(plan) == 0 and not any(v == "low" for v in nutrients.values()):
             plan.append("No major fertilizer adjustment needed")

    return plan


# 📏 FARM SIZE CALCULATION
def calculate_total_fertilizer(fertilizer_plan, farm_size):

    total_plan = []

    try:
        farm_size = float(farm_size)
    except:
        return fertilizer_plan

    for item in fertilizer_plan:

        if "kg/ha" in item:
            parts = item.split("kg/ha")

            try:
                base_qty = float(parts[0].split()[-1])
                total_qty = base_qty * farm_size

                updated = item.replace(
                    f"{base_qty} kg/ha",
                    f"{base_qty} kg/ha (≈ {total_qty:.1f} kg total for {farm_size} ha)"
                )

                total_plan.append(updated)

            except:
                total_plan.append(item)

        else:
            total_plan.append(item)

    return total_plan


# 🚀 MAIN FUNCTION
def analyze_soil(crop, soil_color, previous_yield, fertilizer_used, location=None, farm_size=1):

    nutrients = predict_nutrients(crop, soil_color, previous_yield, fertilizer_used)

    insights = []

    if location:
        nutrients, loc_insights = adjust_by_location(nutrients, location)
        insights.extend(loc_insights)

    if crop:
        nutrients, crop_insights = adjust_by_crop(nutrients, crop)
        insights.extend(crop_insights)

    recommendations = generate_recommendation(nutrients, insights)
    summary = generate_summary(nutrients, crop, insights)

    fertilizer_plan = generate_fertilizer_plan(nutrients, crop, insights)
    fertilizer_plan = calculate_total_fertilizer(fertilizer_plan, farm_size)

    return {
        "status": "success",
        "input": {
            "crop": crop,
            "location": location,
            "farm_size": farm_size
        },
        "nutrient_status": nutrients,
        "insights": insights,
        "recommendations": recommendations,
        "fertilizer_plan": fertilizer_plan,
        "summary": summary
    }