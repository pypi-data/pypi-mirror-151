import{cx as t,cq as e,dU as i,dV as s,_ as r,s as o,e as a,t as l,$ as h,U as n,g as d,i as c,m as u,ar as g,n as b}from"./main-ac83c92b.js";import{z as m,s as v}from"./c.027db416.js";import{E as p,t as _,v as f,w,x as y,y as k,z as S,A as C}from"./c.3e14cfd3.js";import"./c.5756eeee.js";import"./c.8cbd7110.js";class j extends(p(t)){static get template(){return e`
      <style>
        :host {
          user-select: none;
          -webkit-user-select: none;
        }

        #canvas {
          position: relative;
          width: 100%;
          max-width: 330px;
        }
        #canvas > * {
          display: block;
        }
        #interactionLayer {
          color: white;
          position: absolute;
          cursor: crosshair;
          width: 100%;
          height: 100%;
          overflow: visible;
        }
        #backgroundLayer {
          width: 100%;
          overflow: visible;
          --wheel-bordercolor: var(--ha-color-picker-wheel-bordercolor, white);
          --wheel-borderwidth: var(--ha-color-picker-wheel-borderwidth, 3);
          --wheel-shadow: var(
            --ha-color-picker-wheel-shadow,
            rgb(15, 15, 15) 10px 5px 5px 0px
          );
        }

        #marker {
          fill: currentColor;
          stroke: var(--ha-color-picker-marker-bordercolor, white);
          stroke-width: var(--ha-color-picker-marker-borderwidth, 3);
          filter: url(#marker-shadow);
        }
        .dragging #marker {
        }

        #colorTooltip {
          display: none;
          fill: currentColor;
          stroke: var(--ha-color-picker-tooltip-bordercolor, white);
          stroke-width: var(--ha-color-picker-tooltip-borderwidth, 3);
        }

        .touch.dragging #colorTooltip {
          display: inherit;
        }
      </style>
      <div id="canvas">
        <svg id="interactionLayer">
          <defs>
            <filter
              id="marker-shadow"
              x="-50%"
              y="-50%"
              width="200%"
              height="200%"
              filterUnits="objectBoundingBox"
            >
              <feOffset
                result="offOut"
                in="SourceAlpha"
                dx="2"
                dy="2"
              ></feOffset>
              <feGaussianBlur
                result="blurOut"
                in="offOut"
                stdDeviation="2"
              ></feGaussianBlur>
              <feComponentTransfer in="blurOut" result="alphaOut">
                <feFuncA type="linear" slope="0.3"></feFuncA>
              </feComponentTransfer>
              <feBlend
                in="SourceGraphic"
                in2="alphaOut"
                mode="normal"
              ></feBlend>
            </filter>
          </defs>
        </svg>
        <canvas id="backgroundLayer"></canvas>
      </div>
    `}static get properties(){return{hsColor:{type:Object},desiredHsColor:{type:Object,observer:"applyHsColor"},desiredRgbColor:{type:Object,observer:"applyRgbColor"},width:{type:Number,value:500},height:{type:Number,value:500},radius:{type:Number,value:225},hueSegments:{type:Number,value:0,observer:"segmentationChange"},saturationSegments:{type:Number,value:0,observer:"segmentationChange"},ignoreSegments:{type:Boolean,value:!1},throttle:{type:Number,value:500}}}ready(){super.ready(),this.setupLayers(),this.drawColorWheel(),this.drawMarker(),this.desiredHsColor&&this.applyHsColor(this.desiredHsColor),this.desiredRgbColor&&this.applyRgbColor(this.desiredRgbColor),this.interactionLayer.addEventListener("mousedown",(t=>this.onMouseDown(t))),this.interactionLayer.addEventListener("touchstart",(t=>this.onTouchStart(t)))}convertToCanvasCoordinates(t,e){const i=this.interactionLayer.createSVGPoint();i.x=t,i.y=e;const s=i.matrixTransform(this.interactionLayer.getScreenCTM().inverse());return{x:s.x,y:s.y}}onMouseDown(t){const e=this.convertToCanvasCoordinates(t.clientX,t.clientY);this.isInWheel(e.x,e.y)&&(this.onMouseSelect(t),this.canvas.classList.add("mouse","dragging"),this.addEventListener("mousemove",this.onMouseSelect),this.addEventListener("mouseup",this.onMouseUp))}onMouseUp(){this.canvas.classList.remove("mouse","dragging"),this.removeEventListener("mousemove",this.onMouseSelect)}onMouseSelect(t){requestAnimationFrame((()=>this.processUserSelect(t)))}onTouchStart(t){const e=t.changedTouches[0],i=this.convertToCanvasCoordinates(e.clientX,e.clientY);if(this.isInWheel(i.x,i.y)){if(t.target===this.marker)return t.preventDefault(),this.canvas.classList.add("touch","dragging"),this.addEventListener("touchmove",this.onTouchSelect),void this.addEventListener("touchend",this.onTouchEnd);this.tapBecameScroll=!1,this.addEventListener("touchend",this.onTap),this.addEventListener("touchmove",(()=>{this.tapBecameScroll=!0}),{passive:!0})}}onTap(t){this.tapBecameScroll||(t.preventDefault(),this.onTouchSelect(t))}onTouchEnd(){this.canvas.classList.remove("touch","dragging"),this.removeEventListener("touchmove",this.onTouchSelect)}onTouchSelect(t){requestAnimationFrame((()=>this.processUserSelect(t.changedTouches[0])))}processUserSelect(t){const e=this.convertToCanvasCoordinates(t.clientX,t.clientY),s=this.getColor(e.x,e.y);let r;if(this.isInWheel(e.x,e.y))r=this.getRgbColor(e.x,e.y);else{const[t,e,o]=i([s.h,s.s]);r={r:t,g:e,b:o}}this.onColorSelect(s,r)}onColorSelect(t,e){if(this.setMarkerOnColor(t),this.ignoreSegments||(t=this.applySegmentFilter(t)),this.applyColorToCanvas(t),this.colorSelectIsThrottled)return clearTimeout(this.ensureFinalSelect),void(this.ensureFinalSelect=setTimeout((()=>{this.fireColorSelected(t,e)}),this.throttle));this.fireColorSelected(t,e),this.colorSelectIsThrottled=!0,setTimeout((()=>{this.colorSelectIsThrottled=!1}),this.throttle)}fireColorSelected(t,e){this.hsColor=t,this.fire("colorselected",{hs:t,rgb:e})}setMarkerOnColor(t){if(!this.marker||!this.tooltip)return;const e=t.s*this.radius,i=(t.h-180)/180*Math.PI,s=`translate(${-e*Math.cos(i)},${-e*Math.sin(i)})`;this.marker.setAttribute("transform",s),this.tooltip.setAttribute("transform",s)}applyColorToCanvas(t){this.interactionLayer&&(this.interactionLayer.style.color=`hsl(${t.h}, 100%, ${100-50*t.s}%)`)}applyHsColor(t){this.hsColor&&this.hsColor.h===t.h&&this.hsColor.s===t.s||(this.setMarkerOnColor(t),this.ignoreSegments||(t=this.applySegmentFilter(t)),this.hsColor=t,this.applyColorToCanvas(t))}applyRgbColor(t){const[e,i]=s(t);this.applyHsColor({h:e,s:i})}getAngle(t,e){return Math.atan2(-e,-t)/Math.PI*180+180}isInWheel(t,e){return this.getDistance(t,e)<=1}getDistance(t,e){return Math.sqrt(t*t+e*e)/this.radius}getColor(t,e){const i=this.getAngle(t,e),s=this.getDistance(t,e);return{h:i,s:Math.min(s,1)}}getRgbColor(t,e){const i=this.backgroundLayer.getContext("2d").getImageData(t+250,e+250,1,1).data;return{r:i[0],g:i[1],b:i[2]}}applySegmentFilter(t){if(this.hueSegments){const e=360/this.hueSegments,i=e/2;t.h-=i,t.h<0&&(t.h+=360);const s=t.h%e;t.h-=s-e}if(this.saturationSegments)if(1===this.saturationSegments)t.s=1;else{const e=1/this.saturationSegments,i=1/(this.saturationSegments-1),s=Math.floor(t.s/e)*i;t.s=Math.min(s,1)}return t}setupLayers(){this.canvas=this.$.canvas,this.backgroundLayer=this.$.backgroundLayer,this.interactionLayer=this.$.interactionLayer,this.originX=this.width/2,this.originY=this.originX,this.backgroundLayer.width=this.width,this.backgroundLayer.height=this.height,this.interactionLayer.setAttribute("viewBox",`${-this.originX} ${-this.originY} ${this.width} ${this.height}`)}drawColorWheel(){let t,e,i,s;const r=this.backgroundLayer.getContext("2d"),o=this.originX,a=this.originY,l=this.radius,h=window.getComputedStyle(this.backgroundLayer,null),n=parseInt(h.getPropertyValue("--wheel-borderwidth"),10),d=h.getPropertyValue("--wheel-bordercolor").trim(),c=h.getPropertyValue("--wheel-shadow").trim();if("none"!==c){const r=c.split("px ");t=r.pop(),e=parseInt(r[0],10),i=parseInt(r[1],10),s=parseInt(r[2],10)||0}const u=l+n/2,g=l,b=l+n;"none"!==h.shadow&&(r.save(),r.beginPath(),r.arc(o,a,b,0,2*Math.PI,!1),r.shadowColor=t,r.shadowOffsetX=e,r.shadowOffsetY=i,r.shadowBlur=s,r.fillStyle="white",r.fill(),r.restore()),function(t,e){const i=360/(t=t||360),s=i/2;for(let t=0;t<=360;t+=i){const i=(t-s)*(Math.PI/180),l=(t+s+1)*(Math.PI/180);r.beginPath(),r.moveTo(o,a),r.arc(o,a,g,i,l,false),r.closePath();const h=r.createRadialGradient(o,a,0,o,a,g);let n=100;if(h.addColorStop(0,`hsl(${t}, 100%, ${n}%)`),e>0){const i=1/e;let s=0;for(let r=1;r<e;r+=1){const e=n;s=r*i,n=100-50*s,h.addColorStop(s,`hsl(${t}, 100%, ${e}%)`),h.addColorStop(s,`hsl(${t}, 100%, ${n}%)`)}h.addColorStop(s,`hsl(${t}, 100%, 50%)`)}h.addColorStop(1,`hsl(${t}, 100%, 50%)`),r.fillStyle=h,r.fill()}}(this.hueSegments,this.saturationSegments),n>0&&(r.beginPath(),r.arc(o,a,u,0,2*Math.PI,!1),r.lineWidth=n,r.strokeStyle=d,r.stroke())}drawMarker(){const t=this.interactionLayer,e=.08*this.radius,i=.15*this.radius,s=-3*i;t.marker=document.createElementNS("http://www.w3.org/2000/svg","circle"),t.marker.setAttribute("id","marker"),t.marker.setAttribute("r",e),this.marker=t.marker,t.appendChild(t.marker),t.tooltip=document.createElementNS("http://www.w3.org/2000/svg","circle"),t.tooltip.setAttribute("id","colorTooltip"),t.tooltip.setAttribute("r",i),t.tooltip.setAttribute("cx",0),t.tooltip.setAttribute("cy",s),this.tooltip=t.tooltip,t.appendChild(t.tooltip)}segmentationChange(){this.backgroundLayer&&this.drawColorWheel()}}customElements.define("ha-color-picker",j),r([b("more-info-light")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[l()],key:"_brightnessSliderValue",value:()=>0},{kind:"field",decorators:[l()],key:"_ctSliderValue",value:void 0},{kind:"field",decorators:[l()],key:"_cwSliderValue",value:void 0},{kind:"field",decorators:[l()],key:"_wwSliderValue",value:void 0},{kind:"field",decorators:[l()],key:"_wvSliderValue",value:void 0},{kind:"field",decorators:[l()],key:"_colorBrightnessSliderValue",value:void 0},{kind:"field",decorators:[l()],key:"_brightnessAdjusted",value:void 0},{kind:"field",decorators:[l()],key:"_hueSegments",value:()=>24},{kind:"field",decorators:[l()],key:"_saturationSegments",value:()=>8},{kind:"field",decorators:[l()],key:"_colorPickerColor",value:void 0},{kind:"field",decorators:[l()],key:"_mode",value:void 0},{kind:"method",key:"render",value:function(){var t;if(!this.hass||!this.stateObj)return h``;const e=_(this.stateObj,f.COLOR_TEMP),i=_(this.stateObj,f.WHITE),s=_(this.stateObj,f.RGBWW),r=!s&&_(this.stateObj,f.RGBW),o=s||r||w(this.stateObj);return h`
      <div class="content">
        ${y(this.stateObj)?h`
              <ha-labeled-slider
                caption=${this.hass.localize("ui.card.light.brightness")}
                icon="hass:brightness-5"
                min="1"
                max="100"
                value=${this._brightnessSliderValue}
                @change=${this._brightnessSliderChanged}
                pin
              ></ha-labeled-slider>
            `:""}
        ${"on"===this.stateObj.state?h`
              ${e||o?h`<hr />`:""}
              ${o&&(e||i)?h`<ha-button-toggle-group
                    fullWidth
                    .buttons=${this._toggleButtons(e,i)}
                    .active=${this._mode}
                    @value-changed=${this._modeChanged}
                  ></ha-button-toggle-group>`:""}
              ${!e||(o||i)&&this._mode!==f.COLOR_TEMP?"":h`
                    <ha-labeled-slider
                      class="color_temp"
                      caption=${this.hass.localize("ui.card.light.color_temperature")}
                      icon="hass:thermometer"
                      .min=${this.stateObj.attributes.min_mireds}
                      .max=${this.stateObj.attributes.max_mireds}
                      .value=${this._ctSliderValue}
                      @change=${this._ctSliderChanged}
                      pin
                    ></ha-labeled-slider>
                  `}
              ${!o||(e||i)&&"color"!==this._mode?"":h`
                    <div class="segmentationContainer">
                      <ha-color-picker
                        class="color"
                        @colorselected=${this._colorPicked}
                        .desiredRgbColor=${this._colorPickerColor}
                        throttle="500"
                        .hueSegments=${this._hueSegments}
                        .saturationSegments=${this._saturationSegments}
                      >
                      </ha-color-picker>
                      <ha-icon-button
                        .path=${n}
                        @click=${this._segmentClick}
                        class="segmentationButton"
                      ></ha-icon-button>
                    </div>

                    ${r||s?h`<ha-labeled-slider
                          .caption=${this.hass.localize("ui.card.light.color_brightness")}
                          icon="hass:brightness-7"
                          max="100"
                          .value=${this._colorBrightnessSliderValue}
                          @change=${this._colorBrightnessSliderChanged}
                          pin
                        ></ha-labeled-slider>`:""}
                    ${r?h`
                          <ha-labeled-slider
                            .caption=${this.hass.localize("ui.card.light.white_value")}
                            icon="hass:file-word-box"
                            max="100"
                            .name=${"wv"}
                            .value=${this._wvSliderValue}
                            @change=${this._wvSliderChanged}
                            pin
                          ></ha-labeled-slider>
                        `:""}
                    ${s?h`
                          <ha-labeled-slider
                            .caption=${this.hass.localize("ui.card.light.cold_white_value")}
                            icon="hass:file-word-box-outline"
                            max="100"
                            .name=${"cw"}
                            .value=${this._cwSliderValue}
                            @change=${this._wvSliderChanged}
                            pin
                          ></ha-labeled-slider>
                          <ha-labeled-slider
                            .caption=${this.hass.localize("ui.card.light.warm_white_value")}
                            icon="hass:file-word-box"
                            max="100"
                            .name=${"ww"}
                            .value=${this._wwSliderValue}
                            @change=${this._wvSliderChanged}
                            pin
                          ></ha-labeled-slider>
                        `:""}
                  `}
              ${m(this.stateObj,k)&&null!==(t=this.stateObj.attributes.effect_list)&&void 0!==t&&t.length?h`
                    <hr />
                    <ha-select
                      .label=${this.hass.localize("ui.card.light.effect")}
                      .value=${this.stateObj.attributes.effect||""}
                      fixedMenuPosition
                      naturalMenuWidth
                      @selected=${this._effectChanged}
                      @closed=${v}
                    >
                      ${this.stateObj.attributes.effect_list.map((t=>h`
                          <mwc-list-item .value=${t}>
                            ${t}
                          </mwc-list-item>
                        `))}
                    </ha-select>
                  `:""}
            `:""}
        <ha-attributes
          .hass=${this.hass}
          .stateObj=${this.stateObj}
          extra-filters="brightness,color_temp,white_value,effect_list,effect,hs_color,rgb_color,rgbw_color,rgbww_color,xy_color,min_mireds,max_mireds,entity_id,supported_color_modes,color_mode"
        ></ha-attributes>
      </div>
    `}},{kind:"method",key:"willUpdate",value:function(t){if(d(c(i.prototype),"willUpdate",this).call(this,t),!t.has("stateObj"))return;const e=this.stateObj,s=t.get("stateObj");if("on"===e.state){(null==s?void 0:s.entity_id)===e.entity_id&&(null==s?void 0:s.state)===e.state||(this._mode=S(this.stateObj)?"color":this.stateObj.attributes.color_mode);let t=100;if(this._brightnessAdjusted=void 0,e.attributes.color_mode===f.RGB&&!_(e,f.RGBWW)&&!_(e,f.RGBW)){const i=Math.max(...e.attributes.rgb_color);i<255&&(this._brightnessAdjusted=i,t=this._brightnessAdjusted/255*100)}this._brightnessSliderValue=Math.round(e.attributes.brightness*t/255),this._ctSliderValue=e.attributes.color_temp,this._wvSliderValue=e.attributes.color_mode===f.RGBW?Math.round(100*e.attributes.rgbw_color[3]/255):void 0,this._cwSliderValue=e.attributes.color_mode===f.RGBWW?Math.round(100*e.attributes.rgbww_color[3]/255):void 0,this._wwSliderValue=e.attributes.color_mode===f.RGBWW?Math.round(100*e.attributes.rgbww_color[4]/255):void 0;const i=C(e);this._colorBrightnessSliderValue=i?Math.round(100*Math.max(...i.slice(0,3))/255):void 0,this._colorPickerColor=null==i?void 0:i.slice(0,3)}else this._brightnessSliderValue=0}},{kind:"field",key:"_toggleButtons",value:()=>u(((t,e)=>{const i=[{label:"Color",value:"color"}];return t&&i.push({label:"Temperature",value:f.COLOR_TEMP}),e&&i.push({label:"White",value:f.WHITE}),i}))},{kind:"method",key:"_modeChanged",value:function(t){this._mode=t.detail.value}},{kind:"method",key:"_effectChanged",value:function(t){const e=t.target.value;e&&this.stateObj.attributes.effect!==e&&this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,effect:e})}},{kind:"method",key:"_brightnessSliderChanged",value:function(t){const e=Number(t.target.value);if(!isNaN(e))if(this._brightnessSliderValue=e,this._mode!==f.WHITE)if(this._brightnessAdjusted){const t=this.stateObj.attributes.rgb_color||[0,0,0];this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,brightness_pct:e,rgb_color:this._adjustColorBrightness(t,this._brightnessAdjusted,!0)})}else this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,brightness_pct:e});else this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,white:Math.min(255,Math.round(255*e/100))})}},{kind:"method",key:"_ctSliderChanged",value:function(t){const e=Number(t.target.value);isNaN(e)||(this._ctSliderValue=e,this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,color_temp:e}))}},{kind:"method",key:"_wvSliderChanged",value:function(t){const e=t.target;let i=Number(e.value);const s=e.name;if(isNaN(i))return;"wv"===s?this._wvSliderValue=i:"cw"===s?this._cwSliderValue=i:"ww"===s&&(this._wwSliderValue=i),i=Math.min(255,Math.round(255*i/100));const r=C(this.stateObj);if("wv"===s){const t=r||[0,0,0,0];return t[3]=i,void this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,rgbw_color:t})}const o=r||[0,0,0,0,0];for(;o.length<5;)o.push(0);o["cw"===s?3:4]=i,this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,rgbww_color:o})}},{kind:"method",key:"_colorBrightnessSliderChanged",value:function(t){var e;const i=t.target;let s=Number(i.value);if(isNaN(s))return;const r=this._colorBrightnessSliderValue;this._colorBrightnessSliderValue=s,s=255*s/100;const o=(null===(e=C(this.stateObj))||void 0===e?void 0:e.slice(0,3))||[255,255,255];this._setRgbWColor(this._adjustColorBrightness(r?this._adjustColorBrightness(o,255*r/100,!0):o,s))}},{kind:"method",key:"_segmentClick",value:function(){24===this._hueSegments&&8===this._saturationSegments?(this._hueSegments=0,this._saturationSegments=0):(this._hueSegments=24,this._saturationSegments=8)}},{kind:"method",key:"_adjustColorBrightness",value:function(t,e,i=!1){if(void 0!==e&&255!==e){let s=e/255;i&&(s=1/s),t[0]=Math.min(255,Math.round(t[0]*s)),t[1]=Math.min(255,Math.round(t[1]*s)),t[2]=Math.min(255,Math.round(t[2]*s))}return t}},{kind:"method",key:"_setRgbWColor",value:function(t){if(_(this.stateObj,f.RGBWW)){const e=this.stateObj.attributes.rgbww_color?[...this.stateObj.attributes.rgbww_color]:[0,0,0,0,0];this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,rgbww_color:t.concat(e.slice(3))})}else if(_(this.stateObj,f.RGBW)){const e=this.stateObj.attributes.rgbw_color?[...this.stateObj.attributes.rgbw_color]:[0,0,0,0];this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,rgbw_color:t.concat(e.slice(3))})}}},{kind:"method",key:"_colorPicked",value:function(t){if(this._colorPickerColor=[t.detail.rgb.r,t.detail.rgb.g,t.detail.rgb.b],_(this.stateObj,f.RGBWW)||_(this.stateObj,f.RGBW))this._setRgbWColor(this._colorBrightnessSliderValue?this._adjustColorBrightness([t.detail.rgb.r,t.detail.rgb.g,t.detail.rgb.b],255*this._colorBrightnessSliderValue/100):[t.detail.rgb.r,t.detail.rgb.g,t.detail.rgb.b]);else if(_(this.stateObj,f.RGB)){const e=[t.detail.rgb.r,t.detail.rgb.g,t.detail.rgb.b];this._brightnessAdjusted?this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,brightness_pct:this._brightnessSliderValue,rgb_color:this._adjustColorBrightness(e,this._brightnessAdjusted,!0)}):this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,rgb_color:e})}else this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,hs_color:[t.detail.hs.h,100*t.detail.hs.s]})}},{kind:"get",static:!0,key:"styles",value:function(){return g`
      .content {
        display: flex;
        flex-direction: column;
        align-items: center;
      }

      .content > * {
        width: 100%;
      }

      .color_temp {
        --ha-slider-background: -webkit-linear-gradient(
          right,
          rgb(255, 160, 0) 0%,
          white 50%,
          rgb(166, 209, 255) 100%
        );
        /* The color temp minimum value shouldn't be rendered differently. It's not "off". */
        --paper-slider-knob-start-border-color: var(--primary-color);
        margin-bottom: 4px;
      }

      .segmentationContainer {
        position: relative;
        max-height: 500px;
        display: flex;
        justify-content: center;
      }

      ha-button-toggle-group {
        margin-bottom: 8px;
      }

      ha-color-picker {
        --ha-color-picker-wheel-borderwidth: 5;
        --ha-color-picker-wheel-bordercolor: white;
        --ha-color-picker-wheel-shadow: none;
        --ha-color-picker-marker-borderwidth: 2;
        --ha-color-picker-marker-bordercolor: white;
      }

      .segmentationButton {
        position: absolute;
        top: 5%;
        left: 0;
        color: var(--secondary-text-color);
      }

      hr {
        border-color: var(--divider-color);
        border-bottom: none;
        margin: 16px 0;
      }
    `}}]}}),o);
