import{_ as t,s as i,e,t as o,ap as s,$ as n,eD as r,g as a,i as d,m as c,ar as h,n as u}from"./main-ac83c92b.js";import{h as l}from"./c.027db416.js";import{aE as _,bh as f,aG as g,b9 as y,aI as p}from"./c.3e14cfd3.js";import"./c.e38196bb.js";import"./c.8cbd7110.js";t([u("hui-map-card")],(function(t,i){class u extends i{constructor(...i){super(...i),t(this)}}return{F:u,d:[{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e({type:Boolean,reflect:!0})],key:"isPanel",value:()=>!1},{kind:"field",decorators:[o()],key:"_history",value:void 0},{kind:"field",decorators:[o()],key:"_config",value:void 0},{kind:"field",decorators:[s("ha-map")],key:"_map",value:void 0},{kind:"field",key:"_date",value:void 0},{kind:"field",key:"_configEntities",value:void 0},{kind:"field",key:"_colorDict",value:()=>({})},{kind:"field",key:"_colorIndex",value:()=>0},{kind:"method",key:"setConfig",value:function(t){var i;if(!t)throw new Error("Error in card configuration.");if(!(null!==(i=t.entities)&&void 0!==i&&i.length||t.geo_location_sources))throw new Error("Either entities or geo_location_sources must be specified");if(t.entities&&!Array.isArray(t.entities))throw new Error("Entities need to be an array");if(t.geo_location_sources&&!Array.isArray(t.geo_location_sources))throw new Error("Geo_location_sources needs to be an array");this._config=t,this._configEntities=(t.entities?_(t.entities):[]).map((t=>t.entity)),this._cleanupHistory()}},{kind:"method",key:"getCardSize",value:function(){var t;if(null===(t=this._config)||void 0===t||!t.aspect_ratio)return 7;const i=f(this._config.aspect_ratio),e=i&&i.w>0&&i.h>0?`${(100*i.h/i.w).toFixed(2)}`:"100";return 1+Math.floor(Number(e)/25)||3}},{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.ec6e581c.js"),document.createElement("hui-map-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,i,e){return{type:"map",entities:g(t,2,i,e,["device_tracker"])}}},{kind:"method",key:"render",value:function(){var t;return this._config?n`
      <ha-card id="card" .header=${this._config.title}>
        <div id="root">
          <ha-map
            .hass=${this.hass}
            .entities=${this._getEntities(this.hass.states,this._config,this._configEntities)}
            .zoom=${null!==(t=this._config.default_zoom)&&void 0!==t?t:14}
            .paths=${this._getHistoryPaths(this._config,this._history)}
            .darkMode=${this._config.dark_mode}
          ></ha-map>
          <ha-icon-button
            .label=${this.hass.localize("ui.panel.lovelace.cards.map.reset_focus")}
            .path=${r}
            @click=${this._fitMap}
            tabindex="0"
          ></ha-icon-button>
        </div>
      </ha-card>
    `:n``}},{kind:"method",key:"shouldUpdate",value:function(t){if(!t.has("hass")||t.size>1)return!0;const i=t.get("hass");if(!i||!this._configEntities)return!0;if(i.themes.darkMode!==this.hass.themes.darkMode)return!0;for(const t of this._configEntities)if(i.states[t]!==this.hass.states[t])return!0;return!1}},{kind:"method",key:"firstUpdated",value:function(t){a(d(u.prototype),"firstUpdated",this).call(this,t);const i=this.shadowRoot.getElementById("root");if(!this._config||this.isPanel||!i)return;if(!this._config.aspect_ratio)return void(i.style.paddingBottom="100%");const e=f(this._config.aspect_ratio);i.style.paddingBottom=e&&e.w>0&&e.h>0?`${(100*e.h/e.w).toFixed(2)}%`:i.style.paddingBottom="100%"}},{kind:"method",key:"updated",value:function(t){var i,e;null!==(i=this._config)&&void 0!==i&&i.hours_to_show&&null!==(e=this._configEntities)&&void 0!==e&&e.length&&(t.has("_config")||Date.now()-this._date.getTime()>=6e4)&&this._getHistory()}},{kind:"method",key:"_fitMap",value:function(){var t;null===(t=this._map)||void 0===t||t.fitMap()}},{kind:"method",key:"_getColor",value:function(t){let i=this._colorDict[t];return i||(i=y(this._colorIndex),this._colorIndex++,this._colorDict[t]=i,i)}},{kind:"field",key:"_getEntities",value(){return c(((t,i,e)=>{if(!t||!i)return;let o=e||[];if(i.geo_location_sources){const e=[],s=i.geo_location_sources.includes("all");for(const o of Object.values(t))"geo_location"===l(o.entity_id)&&(s||i.geo_location_sources.includes(o.attributes.source))&&e.push(o.entity_id);o=[...o,...e]}return o.map((t=>({entity_id:t,color:this._getColor(t)})))}))}},{kind:"field",key:"_getHistoryPaths",value(){return c(((t,i)=>{if(!t.hours_to_show||!i)return;const e=[];for(const t of i){if((null==t?void 0:t.length)<=1)continue;const i=t.reduce(((t,i)=>{const e=i.attributes.latitude,o=i.attributes.longitude;return e&&o&&t.push([e,o]),t}),[]);e.push({points:i,color:this._getColor(t[0].entity_id),gradualOpacity:.8})}return e}))}},{kind:"method",key:"_getHistory",value:async function(){if(this._date=new Date,!this._configEntities)return;const t=this._configEntities.join(","),i=new Date,e=new Date;e.setHours(i.getHours()-this._config.hours_to_show);const o=await p(this.hass,t,e,i,!1,!1,!1);o.length<1||(this._history=o)}},{kind:"method",key:"_cleanupHistory",value:function(){this._history&&(this._config.hours_to_show<=0?this._history=void 0:this._history=this._history.reduce(((t,i)=>{var e;const o=i[0].entity_id;return null!==(e=this._configEntities)&&void 0!==e&&e.includes(o)&&t.push(i),t}),[]))}},{kind:"get",static:!0,key:"styles",value:function(){return h`
      ha-card {
        overflow: hidden;
        width: 100%;
        height: 100%;
      }

      ha-map {
        z-index: 0;
        border: none;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: inherit;
      }

      ha-icon-button {
        position: absolute;
        top: 75px;
        left: 3px;
        outline: none;
      }

      #root {
        position: relative;
      }

      :host([ispanel]) #root {
        height: 100%;
      }
    `}}]}}),i);
