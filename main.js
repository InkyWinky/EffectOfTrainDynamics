//Extract camera params
//Public variables
let form1 = document.getElementById('camera-param-form');
let resWidth = parseFloat(document.getElementById('res-width').value);
let resHeight = parseFloat(document.getElementById('res-height').value);
let pixelWidth = parseFloat(document.getElementById('pixel-width').value) * 10 ** -3;
let pixelHeight = parseFloat(document.getElementById('pixel-height').value) * 10 ** -3;
let lens = parseFloat(document.getElementById('lens').value);
let workingDist = parseFloat(document.getElementById('working-dist').value);
let speed_kmh = parseFloat(document.getElementById('train-speed-kmh').value);
let image_height = parseFloat(document.getElementById('image-height').value);
console.log(workingDist)
let longFovRes = document.getElementsByClassName('long-fov-result')
let latFovRes = document.getElementsByClassName('lat-fov-result')
let longFovResVal = 2 * workingDist * ((pixelHeight * resHeight / 2) / lens)
let latFovResVal = 2 * workingDist * ((pixelWidth * resWidth / 2) / lens)
let featureSize = parseFloat(document.getElementById('feature-size').value);
for (let i = 0; i < longFovRes.length; i++) {
    longFovRes[i].value = longFovResVal;
}
for (let i = 0; i < latFovRes.length; i++) {
    latFovRes[i].value = latFovResVal;
}

form1.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    //update camera parameters
    resWidth = parseFloat(document.getElementById('res-width').value);
    resHeight = parseFloat(document.getElementById('res-height').value);
    pixelWidth = parseFloat(document.getElementById('pixel-width').value) * 10 ** -3;
    pixelHeight = parseFloat(document.getElementById('pixel-height').value) * 10 ** -3;
    lens = parseFloat(document.getElementById('lens').value);
    workingDist = parseFloat(document.getElementById('working-dist').value);
    longFovResVal = 2 * workingDist * ((pixelHeight * resHeight / 2) / lens)
    latFovResVal = 2 * workingDist * ((pixelWidth * resWidth / 2) / lens)
    for (let i = 0; i < longFovRes.length; i++) {
        longFovRes[i].value = longFovResVal;
    }
    for (let i = 0; i < latFovRes.length; i++) {
        latFovRes[i].value = latFovResVal;
    }

    //update all other errors
    updateVerticalErrorResults();
    updatePitchResults();
    updateYawResults();
    updateTrainSpeed();

});

function findAcquisitionRate(speed, fov) {
    //speed is in km/hr
    //convert speed to m/s
    let speedms = speed * 1000 / 3600
    let acquisitionRate = speedms / (fov * 10 ** -3)
    return acquisitionRate
}

// VERTICAL EFFECT

function findVerticalEffect(newWorkingDist, featureSize) {
    let fov = newWorkingDist * (pixelWidth / lens)
    console.log("new working distance is " + newWorkingDist)
    console.log("new fov is " + fov)
    let pixelDifference = fov - longFovResVal
    console.log("The pixel difference is " + pixelDifference)
    //calculate difference in mm 
    let difference = fov * featureSize - longFovResVal * featureSize
    if (difference < longFovResVal) {
        document.getElementById('vertical-negligible').style.display = "block"
        console.log("The effect is negligible as the error is smaller than the resolution")
    }
    else {
        console.log("not negligible")
        document.getElementById('vertical-negligible').style.display = "none"
    }
    percentDifference = difference / (longFovResVal * featureSize) * 100
    mmDifference = difference
    document.getElementById('vertical-error-perc').value = Math.abs(percentDifference)
    document.getElementById('vertical-error-mm').value = Math.abs(mmDifference)
    console.log("The is size of the feature will be off by " + percentDifference + "%" + "or " + mmDifference + " mm.")
    //acquisition rate change

    let previousAcquisitionRate = findAcquisitionRate(speed_kmh, longFovResVal)
    let newAcquisitionRate = findAcquisitionRate(speed_kmh, fov)
    let acqPercChangeMm = 100 * (previousAcquisitionRate * fov - newAcquisitionRate * fov) / (newAcquisitionRate * fov)
    acqPercDiff = 100 * (newAcquisitionRate - previousAcquisitionRate) / previousAcquisitionRate
    if (newAcquisitionRate > previousAcquisitionRate) {
        document.getElementById('acq-rate-change').textContent = "slower"
    }
    else {
        document.getElementById('acq-rate-change').textContent = "faster"
    }
    document.getElementById('vertical-acquisition-error').value = Math.abs(acqPercDiff)
    document.getElementById('vertical-acquisition').value = Math.abs(newAcquisitionRate)
    document.getElementById('vertical-acq-percent').value = Math.abs(acqPercChangeMm)

}
function updateVerticalErrorResults() {
    let featureSizeChange = ""
    if (parseFloat(document.getElementById('vertical-displacement').value) < 0) {
        featureSizeChange = "larger"
        acqChange = "compressed"
    }
    else {
        featureSizeChange = "smaller"
        acqChange = "elongated"
    }
    document.getElementById('smaller-larger').textContent = featureSizeChange
    document.getElementById('vertical-compress-elongate').textContent = acqChange
    let newWorkingDist = workingDist + parseFloat(document.getElementById('vertical-displacement').value);
    let featureSize = parseFloat(document.getElementById('feature-size').value);
    findVerticalEffect(newWorkingDist, featureSize)

}
let form2 = document.getElementById('vertical-error-form');
form2.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    updateVerticalErrorResults();
});

function updateTrainSpeed() {
    speed_kmh = parseFloat(document.getElementById('train-speed-kmh').value);
    let acquisitionRate = findAcquisitionRate(speed_kmh, longFovResVal);
    document.getElementById('acq-rate').textContent = acquisitionRate.toFixed(4);
    updateVerticalErrorResults();
}

//PITCH ERROR

function updatePitchResults() {
    let pitchAngle = parseFloat(document.getElementById('pitch-angle').value);
    let newWorkingDist = 1100 / (Math.cos(pitchAngle * Math.PI / 180));
    console.log("new working distance from pitch is " + newWorkingDist);
    let skipped_dist_mm = workingDist * Math.tan(pitchAngle * Math.PI / 180);
    let skippedRepeated = "";
    if (pitchAngle > 0) {
        skippedRepeated = "skipped"
    }
    else {
        skippedRepeated = "repeated"
    }
    document.getElementById('skipped-repeated').textContent = skippedRepeated;
    document.getElementById('skipped-rows-mm').value = skipped_dist_mm;

    let new_fov = newWorkingDist * (pixelWidth / lens);
    let pixelDifference = new_fov - longFovResVal
    //calculate difference in mm 
    let difference = new_fov * featureSize - longFovResVal * featureSize

    let percentDifference = difference / (longFovResVal * featureSize) * 100
    document.getElementById('pitch-new-working-dist').value = Math.abs(newWorkingDist) - workingDist
    document.getElementById('pitch-vertical-error-perc').value = Math.abs(percentDifference)
    document.getElementById('pitch-vertical-error-mm').value = Math.abs(difference)

}

//YAW ERROR
function updateYawResults() {
    let yawAngle = parseFloat(document.getElementById('yaw-angle').value);
    let hor_pos = parseFloat(document.getElementById('yaw-hor-pos').value);

    vertical_skip = hor_pos * Math.tan(yawAngle * Math.PI / 180);
    document.getElementById('yaw-vertical-skip-mm').value = vertical_skip;
    document.getElementById('yaw-hor-pos-value').textContent = hor_pos;
}

//ROLL ERROR
function updateRollResults() {
    let rollAngle = parseFloat(document.getElementById('roll-angle').value);

    if (rollAngle > 0) {
        document.getElementById('roll-missing-side').textContent = "left";
        document.getElementById('roll-extended-side').textContent = "right";
    }
    else {
        document.getElementById('roll-missing-side').textContent = "right"
        document.getElementById('roll-extended-side').textContent = "left";
    }
    rollAngle = Math.abs(rollAngle);
    prev_opp = latFovResVal;
}
//show table of contents after scrolling past start
sticky_contents_table = document.getElementById("sticky-contents");

var myScrollFunc = function () {
    var y = window.scrollY;
    console.log(y)
    if (y >= 420) {
        sticky_contents_table.style.display = "block";
        console.log("display: " + sticky_contents_table.style.display)
    } else {
        sticky_contents_table.style.display = "none";
    }
};


window.addEventListener("scroll", myScrollFunc);