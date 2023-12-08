const { PolynomialFeatures } = require('@rainij/polynomial-regression-js');

const axios = require('axios');

function fuelConversion(fuel) {
    const g = 3.785411784; // liters per gallon
    const m = 1609.344; // meters per mile
    const kpg = (g / m * 1000); // kilometers per gallon 
    return 100 / fuel * kpg; // returns fuel as mpg to l/100km or vice versa
}

async function predictFuelConsumptionL100Km(weightKg, year) {
    const weightLbs = weightKg * 2.205;
    const yearMod100 = year % 100;

    const input = [
        [weightLbs, yearMod100]
    ];

    let polyFeatures = new PolynomialFeatures(2);

    console.log("Input:", input);
    const transformedInput = polyFeatures.fitTransform(input);

    const [a, b, c, d, e, f] = transformedInput[0];
    const transformedInputReordered = [[f, c, e, a, b, d]];

    const inferenceInput = {
        'instances': transformedInputReordered
    };

    try {
        const response = await axios.post(
            "http://<Public Kubeflow Endpoint>/kserve/v1/models/sklearn-mpg:predict",
            inferenceInput,
            {
                headers: {
                    "Host": "sklearn-mpg.kserve-deploy-test.example.com"
                }
            }
        );

        const mpg = response.data.predictions[0];
        return fuelConversion(mpg);
    } catch (error) {
        console.error("Error:", error.message);
        throw error;
    }
}

async function run() {
    try {
        const result = await predictFuelConsumptionL100Km(weightKg=(970 + 110), year=1971);
        console.log("Result:", result);
    } catch (error) {
        // Handle errors if necessary
        console.error("Error:", error.message);
    }
}

run();