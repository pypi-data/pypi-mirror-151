import{_ as e,s as r,e as a,t,$ as i,ev as o,ew as s,bg as c,dv as n,ex as l,em as d,eo as h,aq as g,b4 as v,ey as p,bw as y,bu as u,ar as f,n as m}from"./main-ac83c92b.js";import{b1 as b,Q as k}from"./c.3e14cfd3.js";import{g as $,e as x,b as _}from"./c.9e1e758b.js";import{S as w}from"./c.02ed471c.js";import"./c.027db416.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";import"./c.d4761680.js";e([m("hui-energy-distribution-card")],(function(e,r){return{F:class extends r{constructor(...r){super(...r),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"_config",value:void 0},{kind:"field",decorators:[t()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"hassSubscribe",value:function(){var e;return[$(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"render",value:function(){var e,r;if(!this._config)return i``;if(!this._data)return i`${this.hass.localize("ui.panel.lovelace.cards.energy.loading")}`;const a=this._data.prefs,t=x(a),f=void 0!==t.solar,m=void 0!==t.battery,$=void 0!==t.gas,w=t.grid[0].flow_to.length>0,M=null!==(e=b(this._data.stats,t.grid[0].flow_from.map((e=>e.stat_energy_from))))&&void 0!==e?e:0;let z=null;var j;$&&(z=null!==(j=b(this._data.stats,t.gas.map((e=>e.stat_energy_from))))&&void 0!==j?j:0);let C=null;f&&(C=b(this._data.stats,t.solar.map((e=>e.stat_energy_from)))||0);let F=null,D=null;m&&(F=b(this._data.stats,t.battery.map((e=>e.stat_energy_to)))||0,D=b(this._data.stats,t.battery.map((e=>e.stat_energy_from)))||0);let W=null;w&&(W=b(this._data.stats,t.grid[0].flow_to.map((e=>e.stat_energy_to)))||0);let P=null;f&&(P=(C||0)-(W||0)-(F||0));let S=null,E=null;null!==P&&P<0&&(m&&(S=-1*P,S>M&&(E=Math.min(0,S-M),S=M)),P=0);let B=null;f&&m?(E||(E=Math.max(0,(W||0)-(C||0)-(F||0)-(S||0))),B=F-(S||0)):!f&&m&&(E=W);let q=null;m&&(q=(D||0)-(E||0));const H=Math.max(0,M-(S||0)),R=Math.max(0,H+(P||0)+(q||0));let A,O,Q,T,V;f&&(A=P/R*238.76104),q&&(O=q/R*238.76104);let Y="https://app.electricitymap.org";if(this._data.co2SignalEntity&&this._data.fossilEnergyConsumption){const e=Object.values(this._data.fossilEnergyConsumption).reduce(((e,r)=>e+r),0),r=this.hass.states[this._data.co2SignalEntity];if(null!=r&&r.attributes.country_code&&(Y+=`/zone/${r.attributes.country_code}`),null!==e){let r;Q=M-e,r=H!==M?e*(H/M):e,V=r/R*238.76104,T=238.76104-(A||0)-(O||0)-V}}const G=H+(P||0)+(W?W-(E||0):0)+(B||0)+(q||0)+(S||0)+(E||0);return i`
      <ha-card .header=${this._config.title}>
        <div class="card-content">
          ${void 0!==Q||f||$?i`<div class="row">
                ${void 0===Q?i`<div class="spacer"></div>`:i`<div class="circle-container low-carbon">
                      <span class="label"
                        >${this.hass.localize("ui.panel.lovelace.cards.energy.energy_distribution.non_fossil")}</span
                      >
                      <a
                        class="circle"
                        href=${Y}
                        target="_blank"
                        rel="noopener no referrer"
                      >
                        <ha-svg-icon .path=${o}></ha-svg-icon>
                        ${Q?k(Q,this.hass.locale,{maximumFractionDigits:1}):"—"}
                        kWh
                      </a>
                      <svg width="80" height="30">
                        <line x1="40" y1="0" x2="40" y2="30"></line>
                      </svg>
                    </div>`}
                ${f?i`<div class="circle-container solar">
                      <span class="label"
                        >${this.hass.localize("ui.panel.lovelace.cards.energy.energy_distribution.solar")}</span
                      >
                      <div class="circle">
                        <ha-svg-icon .path=${s}></ha-svg-icon>
                        ${k(C||0,this.hass.locale,{maximumFractionDigits:1})}
                        kWh
                      </div>
                    </div>`:$?i`<div class="spacer"></div>`:""}
                ${$?i`<div class="circle-container gas">
                      <span class="label"
                        >${this.hass.localize("ui.panel.lovelace.cards.energy.energy_distribution.gas")}</span
                      >
                      <div class="circle">
                        <ha-svg-icon .path=${c}></ha-svg-icon>
                        ${k(z||0,this.hass.locale,{maximumFractionDigits:1})}
                        ${_(this.hass,a)||"m³"}
                      </div>
                      <svg width="80" height="30">
                        <path d="M40 0 v30" id="gas" />
                        ${z?n`<circle
                    r="1"
                    class="gas"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="2s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#gas" />
                    </animateMotion>
                  </circle>`:""}
                      </svg>
                    </div>`:i`<div class="spacer"></div>`}
              </div>`:""}
          <div class="row">
            <div class="circle-container grid">
              <div class="circle">
                <ha-svg-icon .path=${l}></ha-svg-icon>
                ${null!==W?i`<span class="return">
                      <ha-svg-icon
                        class="small"
                        .path=${d}
                      ></ha-svg-icon
                      >${k(W,this.hass.locale,{maximumFractionDigits:1})}
                      kWh
                    </span>`:""}
                <span class="consumption">
                  ${w?i`<ha-svg-icon
                        class="small"
                        .path=${h}
                      ></ha-svg-icon>`:""}${k(M,this.hass.locale,{maximumFractionDigits:1})}
                  kWh
                </span>
              </div>
              <span class="label"
                >${this.hass.localize("ui.panel.lovelace.cards.energy.energy_distribution.grid")}</span
              >
            </div>
            <div class="circle-container home">
              <div
                class="circle ${g({border:void 0===A&&void 0===T})}"
              >
                <ha-svg-icon .path=${v}></ha-svg-icon>
                ${k(R,this.hass.locale,{maximumFractionDigits:1})}
                kWh
                ${void 0!==A||void 0!==T?i`<svg>
                      ${void 0!==A?n`<circle
                            class="solar"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${A} ${238.76104-A}"
                            shape-rendering="geometricPrecision"
                            stroke-dashoffset="-${238.76104-A}"
                          />`:""}
                      ${O?n`<circle
                            class="battery"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${O} ${238.76104-O}"
                            stroke-dashoffset="-${238.76104-O-(A||0)}"
                            shape-rendering="geometricPrecision"
                          />`:""}
                      ${T?n`<circle
                            class="low-carbon"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${T} ${238.76104-T}"
                            stroke-dashoffset="-${238.76104-T-(O||0)-(A||0)}"
                            shape-rendering="geometricPrecision"
                          />`:""}
                      <circle
                        class="grid"
                        cx="40"
                        cy="40"
                        r="38"
                        stroke-dasharray="${null!==(r=V)&&void 0!==r?r:238.76104-A-(O||0)} ${void 0!==V?238.76104-V:A+(O||0)}"
                        stroke-dashoffset="0"
                        shape-rendering="geometricPrecision"
                      />
                    </svg>`:""}
              </div>
              <span class="label"
                >${this.hass.localize("ui.panel.lovelace.cards.energy.energy_distribution.home")}</span
              >
            </div>
          </div>
          ${m?i`<div class="row">
                <div class="spacer"></div>
                <div class="circle-container battery">
                  <div class="circle">
                    <ha-svg-icon .path=${p}></ha-svg-icon>
                    <span class="battery-in">
                      <ha-svg-icon
                        class="small"
                        .path=${y}
                      ></ha-svg-icon
                      >${k(F||0,this.hass.locale,{maximumFractionDigits:1})}
                      kWh</span
                    >
                    <span class="battery-out">
                      <ha-svg-icon
                        class="small"
                        .path=${u}
                      ></ha-svg-icon>
                      ${k(D||0,this.hass.locale,{maximumFractionDigits:1})}
                      kWh</span
                    >
                  </div>
                  <span class="label"
                    >${this.hass.localize("ui.panel.lovelace.cards.energy.energy_distribution.battery")}</span
                  >
                </div>
                <div class="spacer"></div>
              </div>`:""}
          <div class="lines ${g({battery:m})}">
            <svg
              viewBox="0 0 100 100"
              xmlns="http://www.w3.org/2000/svg"
              preserveAspectRatio="xMidYMid slice"
            >
              ${w&&f?n`<path
                    id="return"
                    class="return"
                    d="M${m?45:47},0 v15 c0,${m?"35 -10,30 -30,30":"40 -10,35 -30,35"} h-20"
                    vector-effect="non-scaling-stroke"
                  ></path> `:""}
              ${f?n`<path
                    id="solar"
                    class="solar"
                    d="M${m?55:53},0 v15 c0,${m?"35 10,30 30,30":"40 10,35 30,35"} h20"
                    vector-effect="non-scaling-stroke"
                  ></path>`:""}
              ${m?n`<path
                    id="battery-house"
                    class="battery-house"
                    d="M55,100 v-15 c0,-35 10,-30 30,-30 h20"
                    vector-effect="non-scaling-stroke"
                  ></path>
                  <path
                    id="battery-grid"
                    class=${g({"battery-from-grid":Boolean(S),"battery-to-grid":Boolean(E)})}
                    d="M45,100 v-15 c0,-35 -10,-30 -30,-30 h-20"
                    vector-effect="non-scaling-stroke"
                  ></path>
                  `:""}
              ${m&&f?n`<path
                    id="battery-solar"
                    class="battery-solar"
                    d="M50,0 V100"
                    vector-effect="non-scaling-stroke"
                  ></path>`:""}
              <path
                class="grid"
                id="grid"
                d="M0,${m?50:f?56:53} H100"
                vector-effect="non-scaling-stroke"
              ></path>
              ${W&&f?n`<circle
                    r="1"
                    class="return"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-(W-(E||0))/G*6}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#return" />
                    </animateMotion>
                  </circle>`:""}
              ${P?n`<circle
                    r="1"
                    class="solar"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-P/G*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#solar" />
                    </animateMotion>
                  </circle>`:""}
              ${H?n`<circle
                    r="1"
                    class="grid"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-H/G*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#grid" />
                    </animateMotion>
                  </circle>`:""}
              ${B?n`<circle
                    r="1"
                    class="battery-solar"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-B/G*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-solar" />
                    </animateMotion>
                  </circle>`:""}
              ${q?n`<circle
                    r="1"
                    class="battery-house"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-q/G*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-house" />
                    </animateMotion>
                  </circle>`:""}
              ${S?n`<circle
                    r="1"
                    class="battery-from-grid"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-S/G*5}s"
                      repeatCount="indefinite"
                      keyPoints="1;0" keyTimes="0;1"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-grid" />
                    </animateMotion>
                  </circle>`:""}
              ${E?n`<circle
                    r="1"
                    class="battery-to-grid"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-E/G*5}s"
                      repeatCount="indefinite"
                      calcMode="linear"
                    >
                      <mpath xlink:href="#battery-grid" />
                    </animateMotion>
                  </circle>`:""}
            </svg>
          </div>
        </div>
        ${this._config.link_dashboard?i`
              <div class="card-actions">
                <a href="/energy"
                  ><mwc-button>
                    ${this.hass.localize("ui.panel.lovelace.cards.energy.energy_distribution.go_to_energy_dashboard")}
                  </mwc-button></a
                >
              </div>
            `:""}
      </ha-card>
    `}},{kind:"field",static:!0,key:"styles",value:()=>f`
    :host {
      --mdc-icon-size: 24px;
    }
    .card-content {
      position: relative;
    }
    .lines {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 146px;
      display: flex;
      justify-content: center;
      padding: 0 16px 16px;
      box-sizing: border-box;
    }
    .lines.battery {
      bottom: 100px;
      height: 156px;
    }
    .lines svg {
      width: calc(100% - 160px);
      height: 100%;
      max-width: 340px;
    }
    .row {
      display: flex;
      justify-content: space-between;
      max-width: 500px;
      margin: 0 auto;
    }
    .circle-container {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .circle-container.low-carbon {
      margin-right: 4px;
    }
    .circle-container.solar {
      margin: 0 4px;
      height: 130px;
    }
    .circle-container.gas {
      margin-left: 4px;
      height: 130px;
    }
    .circle-container.battery {
      height: 110px;
      justify-content: flex-end;
    }
    .spacer {
      width: 84px;
    }
    .circle {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      box-sizing: border-box;
      border: 2px solid;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-size: 12px;
      line-height: 12px;
      position: relative;
      text-decoration: none;
      color: var(--primary-text-color);
    }
    ha-svg-icon {
      padding-bottom: 2px;
    }
    ha-svg-icon.small {
      --mdc-icon-size: 12px;
    }
    .label {
      color: var(--secondary-text-color);
      font-size: 12px;
    }
    line,
    path {
      stroke: var(--primary-text-color);
      stroke-width: 1;
      fill: none;
    }
    .circle svg {
      position: absolute;
      fill: none;
      stroke-width: 4px;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
    }
    .gas path,
    .gas circle {
      stroke: var(--energy-gas-color);
    }
    circle.gas {
      stroke-width: 4;
      fill: var(--energy-gas-color);
    }
    .gas .circle {
      border-color: var(--energy-gas-color);
    }
    .low-carbon line {
      stroke: var(--energy-non-fossil-color);
    }
    .low-carbon .circle {
      border-color: var(--energy-non-fossil-color);
    }
    .low-carbon ha-svg-icon {
      color: var(--energy-non-fossil-color);
    }
    circle.low-carbon {
      stroke: var(--energy-non-fossil-color);
      fill: var(--energy-non-fossil-color);
    }
    .solar .circle {
      border-color: var(--energy-solar-color);
    }
    circle.solar,
    path.solar {
      stroke: var(--energy-solar-color);
    }
    circle.solar {
      stroke-width: 4;
      fill: var(--energy-solar-color);
    }
    .battery .circle {
      border-color: var(--energy-battery-in-color);
    }
    circle.battery,
    path.battery {
      stroke: var(--energy-battery-out-color);
    }
    path.battery-house,
    circle.battery-house {
      stroke: var(--energy-battery-out-color);
    }
    circle.battery-house {
      stroke-width: 4;
      fill: var(--energy-battery-out-color);
    }
    path.battery-solar,
    circle.battery-solar {
      stroke: var(--energy-battery-in-color);
    }
    circle.battery-solar {
      stroke-width: 4;
      fill: var(--energy-battery-in-color);
    }
    .battery-in {
      color: var(--energy-battery-in-color);
    }
    .battery-out {
      color: var(--energy-battery-out-color);
    }
    path.battery-from-grid {
      stroke: var(--energy-grid-consumption-color);
    }
    path.battery-to-grid {
      stroke: var(--energy-grid-return-color);
    }
    path.return,
    circle.return,
    circle.battery-to-grid {
      stroke: var(--energy-grid-return-color);
    }
    circle.return,
    circle.battery-to-grid {
      stroke-width: 4;
      fill: var(--energy-grid-return-color);
    }
    .return {
      color: var(--energy-grid-return-color);
    }
    .grid .circle {
      border-color: var(--energy-grid-consumption-color);
    }
    .consumption {
      color: var(--energy-grid-consumption-color);
    }
    circle.grid,
    circle.battery-from-grid,
    path.grid {
      stroke: var(--energy-grid-consumption-color);
    }
    circle.grid,
    circle.battery-from-grid {
      stroke-width: 4;
      fill: var(--energy-grid-consumption-color);
    }
    .home .circle {
      border-width: 0;
      border-color: var(--primary-color);
    }
    .home .circle.border {
      border-width: 2px;
    }
    .circle svg circle {
      animation: rotate-in 0.6s ease-in;
      transition: stroke-dashoffset 0.4s, stroke-dasharray 0.4s;
      fill: none;
    }
    @keyframes rotate-in {
      from {
        stroke-dashoffset: 238.76104;
        stroke-dasharray: 238.76104;
      }
    }
    .card-actions a {
      text-decoration: none;
    }
  `}]}}),w(r));
