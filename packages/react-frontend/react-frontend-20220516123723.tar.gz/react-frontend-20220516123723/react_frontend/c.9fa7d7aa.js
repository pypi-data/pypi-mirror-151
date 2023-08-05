import{_ as e,s as t,e as a,t as s,g as l,i,dv as o,aA as r,ar as d,n}from"./main-ac83c92b.js";import{Q as h}from"./c.3e14cfd3.js";import{au as c}from"./c.027db416.js";const u=(e,t,a)=>{const s=((e,t,a)=>100*(e-t)/(a-t))(((e,t,a)=>isNaN(e)||isNaN(t)||isNaN(a)?0:e>a?a:e<t?t:e)(e,t,a),t,a);return 180*s/100};e([n("ha-gauge")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[a({type:Number})],key:"min",value:()=>0},{kind:"field",decorators:[a({type:Number})],key:"max",value:()=>100},{kind:"field",decorators:[a({type:Number})],key:"value",value:()=>0},{kind:"field",decorators:[a({type:String})],key:"valueText",value:void 0},{kind:"field",decorators:[a()],key:"locale",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"needle",value:void 0},{kind:"field",decorators:[a()],key:"levels",value:void 0},{kind:"field",decorators:[a()],key:"label",value:()=>""},{kind:"field",decorators:[s()],key:"_angle",value:()=>0},{kind:"field",decorators:[s()],key:"_updated",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(e){l(i(n.prototype),"firstUpdated",this).call(this,e),c((()=>{this._updated=!0,this._angle=u(this.value,this.min,this.max),this._rescale_svg()}))}},{kind:"method",key:"updated",value:function(e){l(i(n.prototype),"updated",this).call(this,e),this._updated&&e.has("value")&&(this._angle=u(this.value,this.min,this.max),this._rescale_svg())}},{kind:"method",key:"render",value:function(){return o`
      <svg viewBox="-50 -50 100 50" class="gauge">
        ${this.needle&&this.levels?"":o`<path
          class="dial"
          d="M -40 0 A 40 40 0 0 1 40 0"
        ></path>`}

        ${this.levels?this.levels.sort(((e,t)=>e.level-t.level)).map(((e,t)=>{let a;if(0===t&&e.level!==this.min){const e=u(this.min,this.min,this.max);a=o`<path
                        stroke="var(--info-color)"
                        class="level"
                        d="M
                          ${0-40*Math.cos(e*Math.PI/180)}
                          ${0-40*Math.sin(e*Math.PI/180)}
                         A 40 40 0 0 1 40 0
                        "
                      ></path>`}const s=u(e.level,this.min,this.max);return o`${a}<path
                      stroke="${e.stroke}"
                      class="level"
                      d="M
                        ${0-40*Math.cos(s*Math.PI/180)}
                        ${0-40*Math.sin(s*Math.PI/180)}
                       A 40 40 0 0 1 40 0
                      "
                    ></path>`})):""}
        ${this.needle?o`<path
                class="needle"
                d="M -25 -2.5 L -47.5 0 L -25 2.5 z"
                style=${r({transform:`rotate(${this._angle}deg)`})}
              >
              `:o`<path
                class="value"
                d="M -40 0 A 40 40 0 1 0 40 0"
                style=${r({transform:`rotate(${this._angle}deg)`})}
              >`}
        </path>
      </svg>
      <svg class="text">
        <text class="value-text">
          ${this.valueText||h(this.value,this.locale)} ${this.label}
        </text>
      </svg>`}},{kind:"method",key:"_rescale_svg",value:function(){const e=this.shadowRoot.querySelector(".text"),t=e.querySelector("text").getBBox();e.setAttribute("viewBox",`${t.x} ${t.y} ${t.width} ${t.height}`)}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        position: relative;
      }
      .dial {
        fill: none;
        stroke: var(--primary-background-color);
        stroke-width: 15;
      }
      .value {
        fill: none;
        stroke-width: 15;
        stroke: var(--gauge-color);
        transition: all 1s ease 0s;
      }
      .needle {
        fill: var(--primary-text-color);
        transition: all 1s ease 0s;
      }
      .level {
        fill: none;
        stroke-width: 15;
      }
      .gauge {
        display: block;
      }
      .text {
        position: absolute;
        max-height: 40%;
        max-width: 55%;
        left: 50%;
        bottom: -6%;
        transform: translate(-50%, 0%);
      }
      .value-text {
        font-size: 50px;
        fill: var(--primary-text-color);
        text-anchor: middle;
      }
    `}}]}}),t);
