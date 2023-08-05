import{eq as e,er as i,c9 as t,ca as s,ac as a,es as n,_ as o,s as r,e as c,t as d,m as h,$ as u,aq as l,g as f,i as _,di as m,d as g,ar as v,n as p}from"./main-ac83c92b.js";import{T as k,h as b,U as y,Y as $,g as x,Z as w}from"./c.027db416.js";import{Q as j}from"./c.3e14cfd3.js";import{s as A}from"./c.85c615ca.js";import{a as I,s as z}from"./c.39da0aeb.js";import{S as D}from"./c.02ed471c.js";import"./c.8cbd7110.js";import"./c.cfa85e17.js";const N=["sensor"],S=["binary_sensor"],B=["light","switch","fan"],E=["camera"],O={sensor:["temperature"],binary_sensor:["motion"]},C={light:{on:e,off:i},switch:{on:t,off:s},fan:{on:k("fan"),off:k("fan")},sensor:{humidity:a},binary_sensor:{motion:n}};let q=o([p("hui-area-card")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.6da0cd40.js"),document.createElement("hui-area-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:async function(e){var i;return{type:"area",area:(null===(i=(await A(e.connection,I))[0])||void 0===i?void 0:i.area_id)||""}}},{kind:"field",decorators:[c({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"_config",value:void 0},{kind:"field",decorators:[d()],key:"_entities",value:void 0},{kind:"field",decorators:[d()],key:"_devices",value:void 0},{kind:"field",decorators:[d()],key:"_areas",value:void 0},{kind:"field",key:"_entitiesByDomain",value:()=>h(((e,i,t,s)=>{const a=t.filter((t=>!t.entity_category&&(t.area_id?t.area_id===e:t.device_id&&i.has(t.device_id)))).map((e=>e.entity_id)),n={};for(const e of a){const i=b(e);if(!(B.includes(i)||N.includes(i)||S.includes(i)||E.includes(i)))continue;const t=s[e];t&&((!N.includes(i)&&!S.includes(i)||O[i].includes(t.attributes.device_class||""))&&(i in n||(n[i]=[]),n[i].push(t)))}return n}))},{kind:"method",key:"_isOn",value:function(e,i){const t=this._entitiesByDomain(this._config.area,this._devicesInArea(this._config.area,this._devices),this._entities,this.hass.states)[e];if(t)return(i?t.filter((e=>e.attributes.device_class===i)):t).some((e=>!y.includes(e.state)&&!$.includes(e.state)))}},{kind:"method",key:"_average",value:function(e,i){const t=this._entitiesByDomain(this._config.area,this._devicesInArea(this._config.area,this._devices),this._entities,this.hass.states)[e].filter((e=>!i||e.attributes.device_class===i));if(!t)return;let s;const a=t.filter((e=>!(!e.attributes.unit_of_measurement||isNaN(Number(e.state)))&&(s?e.attributes.unit_of_measurement===s:(s=e.attributes.unit_of_measurement,!0))));if(!a.length)return;const n=a.reduce(((e,i)=>e+Number(i.state)),0);return`${j(n/a.length,this.hass.locale,{maximumFractionDigits:1})} ${s}`}},{kind:"field",key:"_area",value:()=>h(((e,i)=>i.find((i=>i.area_id===e))||null))},{kind:"field",key:"_devicesInArea",value:()=>h(((e,i)=>new Set(e?i.filter((i=>i.area_id===e)).map((e=>e.id)):[])))},{kind:"method",key:"hassSubscribe",value:function(){return[I(this.hass.connection,(e=>{this._areas=e})),z(this.hass.connection,(e=>{this._devices=e})),x(this.hass.connection,(e=>{this._entities=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){if(!e.area)throw new Error("Area Required");this._config=e}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.has("_config")||!this._config)return!0;if(e.has("_devicesInArea")||e.has("_areas")||e.has("_entities"))return!0;if(!e.has("hass"))return!1;const i=e.get("hass");if(!i||i.themes!==this.hass.themes||i.locale!==this.hass.locale)return!0;if(!this._devices||!this._devicesInArea(this._config.area,this._devices)||!this._entities)return!1;const t=this._entitiesByDomain(this._config.area,this._devicesInArea(this._config.area,this._devices),this._entities,this.hass.states);for(const e of Object.values(t))for(const t of e)if(i.states[t.entity_id]!==t)return!0;return!1}},{kind:"method",key:"render",value:function(){if(!(this._config&&this.hass&&this._areas&&this._devices&&this._entities))return u``;const e=this._entitiesByDomain(this._config.area,this._devicesInArea(this._config.area,this._devices),this._entities,this.hass.states),i=this._area(this._config.area,this._areas);if(null===i)return u`
        <hui-warning>
          ${this.hass.localize("ui.card.area.area_not_found")}
        </hui-warning>
      `;const t=[];let s;return N.forEach((i=>{i in e&&O[i].forEach((s=>{e[i].some((e=>e.attributes.device_class===s))&&t.push(u`
            ${C[i][s]?u`<ha-svg-icon
                  .path=${C[i][s]}
                ></ha-svg-icon>`:""}
            ${this._average(i,s)}
          `)}))})),this._config.show_camera&&"camera"in e&&(s=e.camera[0].entity_id),u`
      <ha-card class=${i.picture||s?"image":""}>
        ${i.picture||s?u`<hui-image
              .config=${this._config}
              .hass=${this.hass}
              .image=${i.picture?i.picture:void 0}
              .cameraImage=${s}
              aspectRatio="16:9"
            ></hui-image>`:""}

        <div
          class="container ${l({navigate:void 0!==this._config.navigation_path})}"
          @click=${this._handleNavigation}
        >
          <div class="alerts">
            ${S.map((i=>i in e?O[i].map((e=>this._isOn(i,e)?u`
                      ${C[i][e]?u`<ha-svg-icon
                            .path=${C[i][e]}
                          ></ha-svg-icon>`:""}
                    `:"")):""))}
          </div>
          <div class="bottom">
            <div>
              <div class="name">${i.name}</div>
              ${t.length?u`<div class="sensors">${t}</div>`:""}
            </div>
            <div class="buttons">
              ${B.map((i=>{if(!(i in e))return"";const t=this._isOn(i);return B.includes(i)?u`
                      <ha-icon-button
                        class=${t?"on":"off"}
                        .path=${C[i][t?"on":"off"]}
                        .domain=${i}
                        @click=${this._toggle}
                      >
                      </ha-icon-button>
                    `:""}))}
            </div>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"updated",value:function(e){if(f(_(t.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const i=e.get("hass"),s=e.get("_config");(!e.has("hass")||i&&i.themes===this.hass.themes)&&(!e.has("_config")||s&&s.theme===this._config.theme)||m(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"_handleNavigation",value:function(){this._config.navigation_path&&g(this._config.navigation_path)}},{kind:"method",key:"_toggle",value:function(e){e.stopPropagation();const i=e.currentTarget.domain;B.includes(i)&&this.hass.callService(i,this._isOn(i)?"turn_off":"turn_on",void 0,{area_id:this._config.area}),w("light")}},{kind:"get",static:!0,key:"styles",value:function(){return v`
      ha-card {
        overflow: hidden;
        position: relative;
        padding-bottom: 56.25%;
        background-size: cover;
      }

      ha-card.image {
        padding-bottom: 0;
      }

      .container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
          0,
          rgba(33, 33, 33, 0.9) 0%,
          rgba(33, 33, 33, 0) 45%
        );
      }

      ha-card:not(.image) .container::before {
        position: absolute;
        content: "";
        width: 100%;
        height: 100%;
        background-color: var(--sidebar-selected-icon-color);
        opacity: 0.12;
      }

      .sensors {
        color: #e3e3e3;
        font-size: 16px;
        --mdc-icon-size: 24px;
        opacity: 0.6;
        margin-top: 8px;
      }

      .alerts {
        padding: 16px;
      }

      .alerts ha-svg-icon {
        background: var(--accent-color);
        color: var(--text-accent-color, var(--text-primary-color));
        padding: 8px;
        border-radius: 50%;
      }

      .name {
        color: white;
        font-size: 24px;
      }

      .bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px;
      }

      .navigate {
        cursor: pointer;
      }

      ha-icon-button {
        color: white;
        background-color: var(--area-button-color, #727272b2);
        border-radius: 50%;
        margin-left: 8px;
        --mdc-icon-button-size: 44px;
      }
      .on {
        color: var(--paper-item-icon-active-color, #fdd835);
      }
    `}}]}}),D(r));export{q as HuiAreaCard};
