<template>
  <div id="speedometer-1"></div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useGlobalStore } from "../stores/useGlobalStore";

const props = defineProps({
  userPref: {
    type: Object,
    default: {},
  },
});
const globalStore = useGlobalStore();
const elm = ref(null);
const _noOfDev = ref(null);
const _speedPointerArrow = ref(null);
const _speedValueInNumeric = ref(null);
const _speedNobNumbHolder = ref([]);
const _speedometerProperty = ref({
  id: "speedometer-cnt-" + Math.floor(Math.random() * 100000) + 1,
  maxVal: 60,
  divFact: 5,
  dangerLevel: 50,
  initDeg: -45,
  maxDeg: 270,
  speedNobeH: 4,
  speedoNobeW: 95,
  speedoNobeL: 13,
  edgeRadius: 150,
  indicatorRadius: 125,
  indicatorNumbRadius: 90,
  speedPositionTxtWH: 80,
  nobW: 20,
  nobH: 4,
  numbW: 30,
  numbH: 20,
  midNobW: 10,
  midNobH: 3,
  noOfSmallDiv: 2,
  multiplier: 1,
  gagueLabel: "kg",
  initVal: 0,
  dangerColor: "#FF113A",
  bgColor: "#0F0F0F",
  speedValBGColor: "#191919",
  speedValTxtColor: "#fff",
  speedArrowColor: "#48a3cb",
  nobNumbColor: "#eee",
  widthScale: 0.6,
});

onMounted(() => {
  if (typeof props.userPref === "object") {
    for (var prop in props.userPref) {
      _speedometerProperty.value[prop] = props.userPref[prop];
    }
  }

  _noOfDev.value = _speedometerProperty.value.maxVal / _speedometerProperty.value.divFact;
  _creatHtmlsElecments();
  setPosition(_speedometerProperty.value.initVal);
  document.getElementById("speedometer-1").append(elm.value);
  const speedometer = document.getElementById("speedometer-1");
  const elements = speedometer.children;
  Array.from(elements).forEach((element) => {
    element.style.transform = `scale(${_speedometerProperty.value.widthScale})`;
  });

  const speedometerRect = speedometer.getBoundingClientRect();
  const speedometerCntRect = elements[0].getBoundingClientRect();
  speedometer.style.width = `${speedometerCntRect.width}px`;
  speedometer.style.height = `${speedometerCntRect.height}px`;
  elements[0].style.marginLeft = `-${speedometerCntRect.left - speedometerRect.left}px`;
  elements[0].style.marginTop = `-${speedometerCntRect.top - speedometerRect.top}px`;
});

const _creatHtmlsElecments = () => {
  elm.value = _createElm({
    elmType: "div",
    attrs: {
      id: _speedometerProperty.value.id,
      class: "speedometer",
    },
  });
  _setCssProperty();
  _createIndicators();
};
const _createElm = (metedata) => {
  if (!metedata || metedata instanceof Element || metedata instanceof HTMLDocument || typeof metedata === "string") {
    return metedata;
  }
  var $elm = document.createElement(metedata.elmType);
  if (metedata.attrs) {
    for (var i in metedata.attrs) {
      $elm.setAttribute(i, metedata.attrs[i]);
    }
  }
  if (metedata.text) $elm.innerText = metedata.text;
  if (metedata.html) $elm.innerHTML = metedata.html;
  if (metedata.children) {
    for (var j in metedata.children) {
      var chaild = _createElm(metedata.children[j]);
      if (chaild) {
        $elm.append(chaild);
      }
    }
  }
  return $elm;
};
const _setCssProperty = () => {
  var speedoWH = _speedometerProperty.value.edgeRadius * 2,
    speedNobeTop = _speedometerProperty.value.edgeRadius - _speedometerProperty.value.speedNobeH / 2,
    speedNobeAngle = _speedometerProperty.value.initDeg,
    speedPositionTxtTL = _speedometerProperty.value.edgeRadius - _speedometerProperty.value.speedPositionTxtWH / 2;

  var cssIdSelector = "#" + _speedometerProperty.value.id;
  var tempStyleVar = [
    cssIdSelector + ".speedometer{",
    "width  :" + speedoWH + "px;",
    "height :" + speedoWH + "px;",
    "}",
    cssIdSelector + " .speedNobe{",
    "height            :" + _speedometerProperty.value.speedNobeH + "px;",
    "top               :" + speedNobeTop + "px;",
    "transform         :rotate(" + speedNobeAngle + "deg);",
    "-webkit-transform :rotate(" + speedNobeAngle + "deg);",
    "-moz-transform    :rotate(" + speedNobeAngle + "deg);",
    "-o-transform      :rotate(" + speedNobeAngle + "deg);",
    "}",
    cssIdSelector + " .speedPosition{",
    "width  :" + _speedometerProperty.value.speedPositionTxtWH + "px;",
    "height :" + _speedometerProperty.value.speedPositionTxtWH + "px;",
    "top  :" + speedPositionTxtTL + "px;",
    "left :" + speedPositionTxtTL + "px;",
    "}",
    cssIdSelector + " .speedNobe div{",
    "width  :" + _speedometerProperty.value.speedoNobeW + "px;",
    "left :" + _speedometerProperty.value.speedoNobeL + "px;",
    "}",
    cssIdSelector + " .nob{",
    "width  :" + _speedometerProperty.value.nobW + "px;",
    "height :" + _speedometerProperty.value.nobH + "px;",
    "}",
    cssIdSelector + " .numb{",
    "width  :" + _speedometerProperty.value.numbW + "px;",
    "height :" + _speedometerProperty.value.numbH + "px;",
    "}",
    cssIdSelector + " .midNob{",
    "width  :" + _speedometerProperty.value.midNobW + "px;",
    "height :" + _speedometerProperty.value.midNobH + "px;",
    "}",

    //Colors
    cssIdSelector + ".speedometer{",
    "background:" + _speedometerProperty.value.bgColor + ";",
    // "box-shadow: 0 0 30px 1px " + _speedometerProperty.value.bgColor + ";",
    "}",
    cssIdSelector + ".speedometer .speedPosition{",
    "background:" + _speedometerProperty.value.speedValBGColor + ";",
    "color:" + _speedometerProperty.value.speedValTxtColor + ";",
    "box-shadow: 0 0 3px 3px " + _speedometerProperty.value.speedValBGColor + ";",
    "}",
    cssIdSelector + ".speedometer .speedNobe div{",
    "background:" + _speedometerProperty.value.speedArrowColor + ";",
    "}",
    cssIdSelector + ".speedometer .nob{",
    "background:" + _speedometerProperty.value.nobNumbColor + ";",
    "box-shadow: 0 0 2px 1px " + _speedometerProperty.value.nobNumbColor + ";",
    "}",
    cssIdSelector + ".speedometer .numb{",
    "color:" + _speedometerProperty.value.nobNumbColor + ";",
    "}",
    cssIdSelector + ".speedometer .nob.danger{",
    "background:" + _speedometerProperty.value.dangerColor + ";",
    "box-shadow: 0 0 2px 1px " + _speedometerProperty.value.dangerColor + ";",
    "}",
    cssIdSelector + ".speedometer .numb.danger{",
    "color:" + _speedometerProperty.value.dangerColor + ";",
    "}",
  ].join("");

  var styleElm = _createElm({
    elmType: "style",
    attrs: {},
    html: tempStyleVar,
  });

  elm.value.append(styleElm);
};
const _createIndicators = () => {
  var divDeg = _speedometerProperty.value.maxDeg / _noOfDev.value,
    induCatorLinesPosLeft,
    induCatorLinesPosTop,
    induCatorNumbPosLeft,
    induCatorNumbPosTop,
    envelopeElm = elm.value;

  for (var i = 0; i <= _noOfDev.value; i++) {
    var curDig = _speedometerProperty.value.initDeg + i * divDeg;
    var curIndVal = i * _speedometerProperty.value.divFact;
    var dangCls = curIndVal >= _speedometerProperty.value.dangerLevel ? "danger" : "";

    var induCatorLinesPosY = _speedometerProperty.value.indicatorRadius * Math.cos(0.01746 * curDig);
    var induCatorLinesPosX = _speedometerProperty.value.indicatorRadius * Math.sin(0.01746 * curDig);

    var induCatorNumbPosY = _speedometerProperty.value.indicatorNumbRadius * Math.cos(0.01746 * curDig);
    var induCatorNumbPosX = _speedometerProperty.value.indicatorNumbRadius * Math.sin(0.01746 * curDig);

    induCatorNumbPosLeft =
      _speedometerProperty.value.edgeRadius - induCatorNumbPosX - _speedometerProperty.value.numbW / 2;
    induCatorNumbPosTop =
      _speedometerProperty.value.edgeRadius - induCatorNumbPosY - _speedometerProperty.value.numbH / 2;

    var nob, numb;

    var isSuperNob = i % _speedometerProperty.value.noOfSmallDiv === 0;

    if (isSuperNob) {
      induCatorLinesPosLeft = _speedometerProperty.value.edgeRadius - induCatorLinesPosX - 2;
      induCatorLinesPosTop = _speedometerProperty.value.edgeRadius - induCatorLinesPosY - 10;
      induCatorNumbPosLeft =
        _speedometerProperty.value.edgeRadius - induCatorNumbPosX - _speedometerProperty.value.numbW / 2;
      induCatorNumbPosTop =
        _speedometerProperty.value.edgeRadius - induCatorNumbPosY - _speedometerProperty.value.numbH / 2;
    } else {
      induCatorLinesPosLeft =
        _speedometerProperty.value.edgeRadius - induCatorLinesPosX - _speedometerProperty.value.midNobH / 2;
      induCatorLinesPosTop =
        _speedometerProperty.value.edgeRadius - induCatorLinesPosY - _speedometerProperty.value.midNobW / 2;
    }

    nob = _createElm({
      elmType: "div",
      attrs: {
        class: "nob " + dangCls + (isSuperNob ? "" : " midNob"),
        style:
          "left:" +
          induCatorLinesPosTop +
          "px;top:" +
          induCatorLinesPosLeft +
          "px;" +
          "transform:rotate(" +
          curDig +
          "deg);",
      },
    });

    numb = _createElm({
      elmType: "div",
      attrs: {
        class: "numb " + dangCls,
        style: "left:" + induCatorNumbPosTop + "px;top:" + induCatorNumbPosLeft + "px;",
      },
      html: isSuperNob ? String(curIndVal) : "", // mid nob does not have text
    });

    _speedNobNumbHolder.value.push({
      nob: nob,
      numb: numb,
    });

    // Speed indicators arround the circle
    envelopeElm.append(nob, numb);
  }

  // Speed pointer arrow
  _speedPointerArrow.value = _createElm({
    elmType: "div",
    attrs: {
      class: "speedNobe",
    },
    html: "<div></div>",
  });

  // Speed value indicator at the center
  _speedValueInNumeric.value = _createElm({
    elmType: "div",
    attrs: {
      class: "speedPosition",
    },
  });

  envelopeElm.append(_speedPointerArrow.value);
  envelopeElm.append(_speedValueInNumeric.value);
};
const setPosition = (speed) => {
  if (speed > _speedometerProperty.value.maxVal) {
    speed = _speedometerProperty.value.maxVal;
  }
  if (speed < 0 || isNaN(speed)) {
    speed = 0;
  }
  var speedInDeg =
    (_speedometerProperty.value.maxDeg / _speedometerProperty.value.maxVal) * speed +
    _speedometerProperty.value.initDeg;

  // Set Speed arrow indigator position
  _speedPointerArrow.value.style.transform = "rotate(" + speedInDeg + "deg)";

  // Set Speed value at the center of speedometer
  var centerVal = speed * _speedometerProperty.value.multiplier;
  _speedValueInNumeric.value.innerHTML = centerVal + "<br />" + _speedometerProperty.value.gagueLabel;

  // Set indicator nob and number brightness value
  for (var i = 0; i <= _noOfDev.value; i++) {
    var speedNobNumb = _speedNobNumbHolder.value[i];
    if (speed >= i * _speedometerProperty.value.divFact) {
      _addClass(speedNobNumb.nob, "bright");
      _addClass(speedNobNumb.numb, "bright");
    } else {
      _removeClass(speedNobNumb.nob, "bright");
      _removeClass(speedNobNumb.numb, "bright");
    }
  }
};
const _addClass = (elm, className) => {
  var newClass = elm.getAttribute("class").replace(new RegExp(className, "g"), "") + " " + className;
  elm.setAttribute("class", newClass);
};
const _removeClass = (elm, className) => {
  var newClass = elm.getAttribute("class").replace(new RegExp(className, "g"), "");
  elm.setAttribute("class", newClass);
};

watch(
  () => globalStore.weight,
  (newValue, oldValue) => {
    setPosition(newValue);
  }
);
</script>

<style>
.speedometer {
  background: #0f0f0f;
  position: relative;

  border-radius: 50%;
}
.speedometer .speedNobe {
  position: absolute;
  width: 100%;
  z-index: 10;
  transition: all 1s;
}
.speedometer .speedPosition {
  position: absolute;
  text-align: center;
  line-height: 80px;
  font-family: arial;
  font-size: 30px;
  font-weight: bold;
  border-radius: 50%;

  background: #191919;
  color: #fff;
  box-shadow: 0 0 3px 3px black;
}
.speedometer .fonts {
  font-family: arial;
  font-weight: bold;
  width: 100%;
  text-align: center;
}

.speedometer .speedNobe div {
  background: #48a3cb;
  position: absolute;
  height: 100%;
  top: 0;
}
.speedometer .numb,
.nob {
  transition: opacity 1s;
  position: absolute;
  opacity: 0.5;
}
.speedometer .nob {
  background: #eee;
  box-shadow: 0 0 2px 1px #eee;
}
.speedometer .numb {
  color: #eee;
  text-align: left;
  overflow: hidden;
  opacity: 0.5;
  font-family: arial;
  font-size: 16px;
  font-weight: bold;
}
.speedometer .nob.bright {
  opacity: 1;
}
.speedometer .nob.danger {
  background: #ff113a;
  box-shadow: 0 0 2px 1px #ff113a;
}
.speedometer .numb.bright {
  opacity: 1;
}
.speedometer .numb.danger {
  color: #ff113a;
}
</style>
