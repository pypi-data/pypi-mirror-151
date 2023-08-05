import{_ as e,s as t,e as i,$ as a,aA as s,f as o,ar as r,cK as n,t as l,g as d,i as h,n as c}from"./main-ac83c92b.js";import{c as u,a as p}from"./c.027db416.js";import{O as m}from"./c.3e14cfd3.js";const f=(e,t)=>e.tileLayer(`https://{s}.basemaps.cartocdn.com/${t?"dark_all":"light_all"}/{z}/{x}/{y}${e.Browser.retina?"@2x.png":".png"}`,{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20});let y=e(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:"entity-id"})],key:"entityId",value:void 0},{kind:"field",decorators:[i({attribute:"entity-name"})],key:"entityName",value:void 0},{kind:"field",decorators:[i({attribute:"entity-picture"})],key:"entityPicture",value:void 0},{kind:"field",decorators:[i({attribute:"entity-color"})],key:"entityColor",value:void 0},{kind:"method",key:"render",value:function(){return a`
      <div
        class="marker"
        style=${s({"border-color":this.entityColor})}
        @click=${this._badgeTap}
      >
        ${this.entityPicture?a`<div
              class="entity-picture"
              style=${s({"background-image":`url(${this.entityPicture})`})}
            ></div>`:this.entityName}
      </div>
    `}},{kind:"method",key:"_badgeTap",value:function(e){e.stopPropagation(),this.entityId&&o(this,"hass-more-info",{entityId:this.entityId})}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      .marker {
        display: flex;
        justify-content: center;
        align-items: center;
        box-sizing: border-box;
        overflow: hidden;
        width: 48px;
        height: 48px;
        font-size: var(--ha-marker-font-size, 1.5em);
        border-radius: 50%;
        border: 1px solid var(--ha-marker-color, var(--primary-color));
        color: var(--primary-text-color);
        background-color: var(--card-background-color);
      }
      .entity-picture {
        background-size: cover;
        height: 100%;
        width: 100%;
      }
    `}}]}}),t);customElements.define("ha-entity-marker",y);const k=e=>"string"==typeof e?e:e.entity_id;e([c("ha-map")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"entities",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"paths",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"layers",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"autoFit",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"fitZones",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"darkMode",value:void 0},{kind:"field",decorators:[i({type:Number})],key:"zoom",value:()=>14},{kind:"field",decorators:[l()],key:"_loaded",value:()=>!1},{kind:"field",key:"leafletMap",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"field",key:"_tileLayer",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"field",key:"_mapItems",value:()=>[]},{kind:"field",key:"_mapZones",value:()=>[]},{kind:"field",key:"_mapPaths",value:()=>[]},{kind:"method",key:"connectedCallback",value:function(){d(h(a.prototype),"connectedCallback",this).call(this),this._loadMap(),this._attachObserver()}},{kind:"method",key:"disconnectedCallback",value:function(){d(h(a.prototype),"disconnectedCallback",this).call(this),this.leafletMap&&(this.leafletMap.remove(),this.leafletMap=void 0,this.Leaflet=void 0),this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}},{kind:"method",key:"update",value:function(e){var t;if(d(h(a.prototype),"update",this).call(this,e),!this._loaded)return;const i=e.get("hass");if(e.has("_loaded")||e.has("entities"))this._drawEntities();else if(this._loaded&&i&&this.entities)for(const e of this.entities)if(i.states[k(e)]!==this.hass.states[k(e)]){this._drawEntities();break}if((e.has("_loaded")||e.has("paths"))&&this._drawPaths(),(e.has("_loaded")||e.has("layers"))&&this._drawLayers(e.get("layers")),(e.has("_loaded")||(e.has("entities")||e.has("layers"))&&this.autoFit)&&this.fitMap(),e.has("zoom")&&this.leafletMap.setZoom(this.zoom),!e.has("darkMode")&&(!e.has("hass")||i&&i.themes.darkMode===this.hass.themes.darkMode))return;const s=null!==(t=this.darkMode)&&void 0!==t?t:this.hass.themes.darkMode;this._tileLayer=((e,t,i,a)=>(t.removeLayer(i),(i=f(e,a)).addTo(t),i))(this.Leaflet,this.leafletMap,this._tileLayer,s),this.shadowRoot.getElementById("map").classList.toggle("dark",s)}},{kind:"method",key:"_loadMap",value:async function(){var e;let t=this.shadowRoot.getElementById("map");t||(t=document.createElement("div"),t.id="map",this.shadowRoot.append(t));const i=null!==(e=this.darkMode)&&void 0!==e?e:this.hass.themes.darkMode;[this.leafletMap,this.Leaflet,this._tileLayer]=await(async(e,t)=>{if(!e.parentNode)throw new Error("Cannot setup Leaflet map on disconnected element");const i=(await import("./c.3b41e231.js")).default;i.Icon.Default.imagePath="/static/images/leaflet/images/";const a=i.map(e),s=document.createElement("link");return s.setAttribute("href","/static/images/leaflet/leaflet.css"),s.setAttribute("rel","stylesheet"),e.parentNode.appendChild(s),a.setView([52.3731339,4.8903147],13),[a,i,f(i,Boolean(t)).addTo(a)]})(t,i),this.shadowRoot.getElementById("map").classList.toggle("dark",i),this._loaded=!0}},{kind:"method",key:"fitMap",value:function(){var e,t;if(!this.leafletMap||!this.Leaflet||!this.hass)return;if(!(this._mapItems.length||null!==(e=this.layers)&&void 0!==e&&e.length))return void this.leafletMap.setView(new this.Leaflet.LatLng(this.hass.config.latitude,this.hass.config.longitude),this.zoom);let i=this.Leaflet.latLngBounds(this._mapItems?this._mapItems.map((e=>e.getLatLng())):[]);var a;this.fitZones&&(null===(a=this._mapZones)||void 0===a||a.forEach((e=>{i.extend("getBounds"in e?e.getBounds():e.getLatLng())})));null===(t=this.layers)||void 0===t||t.forEach((e=>{i.extend("getBounds"in e?e.getBounds():e.getLatLng())})),this.layers||(i=i.pad(.5)),this.leafletMap.fitBounds(i,{maxZoom:this.zoom})}},{kind:"method",key:"_drawLayers",value:function(e){if(e&&e.forEach((e=>e.remove())),!this.layers)return;const t=this.leafletMap;this.layers.forEach((e=>{t.addLayer(e)}))}},{kind:"method",key:"_drawPaths",value:function(){const e=this.hass,t=this.leafletMap,i=this.Leaflet;if(!e||!t||!i)return;if(this._mapPaths.length&&(this._mapPaths.forEach((e=>e.remove())),this._mapPaths=[]),!this.paths)return;const a=getComputedStyle(this).getPropertyValue("--dark-primary-color");this.paths.forEach((e=>{let s,o;e.gradualOpacity&&(s=e.gradualOpacity/(e.points.length-2),o=1-e.gradualOpacity);for(let t=0;t<e.points.length-1;t++){const r=e.gradualOpacity?o+t*s:void 0;this._mapPaths.push(i.circleMarker(e.points[t],{radius:3,color:e.color||a,opacity:r,fillOpacity:r,interactive:!1})),this._mapPaths.push(i.polyline([e.points[t],e.points[t+1]],{color:e.color||a,opacity:r,interactive:!1}))}const r=e.points.length-1;if(r>=0){const t=e.gradualOpacity?o+r*s:void 0;this._mapPaths.push(i.circleMarker(e.points[r],{radius:3,color:e.color||a,opacity:t,fillOpacity:t,interactive:!1}))}this._mapPaths.forEach((e=>t.addLayer(e)))}))}},{kind:"method",key:"_drawEntities",value:function(){var e;const t=this.hass,i=this.leafletMap,a=this.Leaflet;if(!t||!i||!a)return;if(this._mapItems.length&&(this._mapItems.forEach((e=>e.remove())),this._mapItems=[]),this._mapZones.length&&(this._mapZones.forEach((e=>e.remove())),this._mapZones=[]),!this.entities)return;const s=getComputedStyle(this),o=s.getPropertyValue("--accent-color"),r=s.getPropertyValue("--dark-primary-color"),n=(null!==(e=this.darkMode)&&void 0!==e?e:this.hass.themes.darkMode)?"dark":"light";for(const e of this.entities){const i=t.states[k(e)];if(!i)continue;const s=u(i),{latitude:l,longitude:d,passive:h,icon:c,radius:m,entity_picture:f,gps_accuracy:y}=i.attributes;if(!l||!d)continue;if("zone"===p(i)){if(h)continue;let e="";if(c){const t=document.createElement("ha-icon");t.setAttribute("icon",c),e=t.outerHTML}else{const t=document.createElement("span");t.innerHTML=s,e=t.outerHTML}this._mapZones.push(a.marker([l,d],{icon:a.divIcon({html:e,iconSize:[24,24],className:n}),interactive:!1,title:s})),this._mapZones.push(a.circle([l,d],{interactive:!1,color:o,radius:m}));continue}const v=s.split(" ").map((e=>e[0])).join("").substr(0,3);this._mapItems.push(a.marker([l,d],{icon:a.divIcon({html:`\n              <ha-entity-marker\n                entity-id="${k(e)}"\n                entity-name="${v}"\n                entity-picture="${f?this.hass.hassUrl(f):""}"\n                ${"string"!=typeof e?`entity-color="${e.color}"`:""}\n              ></ha-entity-marker>\n            `,iconSize:[48,48],className:""}),title:u(i)})),y&&this._mapItems.push(a.circle([l,d],{interactive:!1,color:r,radius:y}))}this._mapItems.forEach((e=>i.addLayer(e))),this._mapZones.forEach((e=>i.addLayer(e)))}},{kind:"method",key:"_attachObserver",value:async function(){this._resizeObserver||(await m(),this._resizeObserver=new ResizeObserver((()=>{var e;null===(e=this.leafletMap)||void 0===e||e.invalidateSize({debounceMoveend:!0})}))),this._resizeObserver.observe(this)}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      :host {
        display: block;
        height: 300px;
      }
      #map {
        height: 100%;
      }
      #map.dark {
        background: #090909;
      }
      .light {
        color: #000000;
      }
      .dark {
        color: #ffffff;
      }
      .leaflet-marker-draggable {
        cursor: move !important;
      }
      .leaflet-edit-resize {
        border-radius: 50%;
        cursor: nesw-resize !important;
      }
      .named-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        color: var(--primary-text-color);
      }
      .leaflet-pane {
        z-index: 0 !important;
      }
      .leaflet-control,
      .leaflet-top,
      .leaflet-bottom {
        z-index: 1 !important;
      }
    `}}]}}),n);
