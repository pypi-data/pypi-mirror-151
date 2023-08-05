import{de as e,_ as t,s as i,e as a,t as s,$ as o,g as n,i as r,m as d,f as l,eK as c,ar as h,n as m,ap as u,aq as p,aA as g,b2 as _,ed as v,eL as b,ax as f,au as y,h as k,eM as w,em as x,cD as $,dF as I}from"./main-ac83c92b.js";import{bq as z,a9 as O,br as C,bs as S,O as D,a8 as T}from"./c.3e14cfd3.js";import{ax as H,s as j,k as P,e as A,d as E}from"./c.027db416.js";import"./c.8cbd7110.js";import{b as W,e as L}from"./c.3eb3ee48.js";import{d as U}from"./c.57c0073c.js";import"./c.53212acc.js";import"./c.e9aa747b.js";import"./c.d76504d5.js";import{c as F}from"./c.cfa85e17.js";import"./c.9e7e5aa1.js";const V=(e,t)=>e.callWS({type:"media_source/browse_media",media_content_id:t}),M=e=>e.startsWith("media-source://media_source"),R=async(e,t,i)=>{const a=new FormData;a.append("media_content_id",t),a.append("file",i);const s=await e.fetchWithAuth("/api/media_source/local_source/upload",{method:"POST",body:a});if(413===s.status)throw new Error(`Uploaded file is too large (${i.name})`);if(200!==s.status)throw new Error("Unknown error");return s.json()},N=async(e,t)=>e.callWS({type:"media_source/local_source/remove",media_content_id:t});class q{constructor(t=!0){e(this,"_storage",{}),e(this,"_listeners",{}),t&&window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const t=window.localStorage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const i=this._listeners[e].indexOf(t);-1!==i&&this._listeners[e].splice(i,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){this._storage[e]=t;try{window.localStorage.setItem(e,JSON.stringify(t))}catch(e){}}}const B=new q,K=(e,t,i=!0,a)=>s=>{const o=i?B:new q(!1),n=String(s.key);e=e||String(s.key);const r=s.initializer?s.initializer():void 0;o.addFromStorage(e);const d=()=>o.hasKey(e)?o.getValue(e):r;return{kind:"method",placement:"prototype",key:s.key,descriptor:{set(i){((i,a)=>{let n;t&&(n=d()),o.setValue(e,a),t&&i.requestUpdate(s.key,n)})(this,i)},get:()=>d(),enumerable:!0,configurable:!0},finisher(r){if(t&&i){const t=r.prototype.connectedCallback,i=r.prototype.disconnectedCallback;r.prototype.connectedCallback=function(){var i;t.call(this),this[`__unbsubLocalStorage${n}`]=(i=this,o.subscribeChanges(e,(e=>{i.requestUpdate(s.key,e)})))},r.prototype.disconnectedCallback=function(){i.call(this),this[`__unbsubLocalStorage${n}`]()}}t&&r.createProperty(s.key,{noAccessor:!0,...a})}}},G=e=>{const t=[];if(!e)return t;const i=new Set;for(const[a]of e.languages){if(i.has(a))continue;i.add(a);let e=a;if(a in H.translations)e=H.translations[a].nativeName;else{const[t,i]=a.split("-");t in H.translations&&(e=`${H.translations[t].nativeName}`,t.toLowerCase()!==i.toLowerCase()&&(e+=` (${i})`))}t.push([a,e])}return t.sort(((e,t)=>F(e[1],t[1])))},J=(e,t,i)=>{const a=[];if(!t)return a;for(const[s,o]of t.languages)s===e&&a.push([o,i(`ui.panel.media-browser.tts.gender_${o}`)||i(`ui.panel.config.cloud.account.tts.${o}`)||o]);return a.sort(((e,t)=>F(e[1],t[1])))};t([m("ha-browse-media-tts")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[a()],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"item",value:void 0},{kind:"field",decorators:[a()],key:"action",value:void 0},{kind:"field",decorators:[s()],key:"_cloudDefaultOptions",value:void 0},{kind:"field",decorators:[s()],key:"_cloudOptions",value:void 0},{kind:"field",decorators:[s()],key:"_cloudTTSInfo",value:void 0},{kind:"field",decorators:[K("cloudTtsTryMessage",!0,!1)],key:"_message",value:void 0},{kind:"method",key:"render",value:function(){var e;return o`<ha-card>
      <div class="card-content">
        <ha-textarea
          autogrow
          .label=${this.hass.localize("ui.components.media-browser.tts.message")}
          .value=${this._message||this.hass.localize("ui.components.media-browser.tts.example_message",{name:(null===(e=this.hass.user)||void 0===e?void 0:e.name)||""})}
        >
        </ha-textarea>
        ${this._cloudDefaultOptions?this._renderCloudOptions():""}
      </div>
      <div class="card-actions">
        ${!this._cloudDefaultOptions||this._cloudDefaultOptions[0]===this._cloudOptions[0]&&this._cloudDefaultOptions[1]===this._cloudOptions[1]?o`<span></span>`:o`
              <button class="link" @click=${this._storeDefaults}>
                ${this.hass.localize("ui.components.media-browser.tts.set_as_default")}
              </button>
            `}

        <mwc-button @click=${this._ttsClicked}>
          ${this.hass.localize(`ui.components.media-browser.tts.action_${this.action}`)}
        </mwc-button>
      </div>
    </ha-card> `}},{kind:"method",key:"_renderCloudOptions",value:function(){if(!this._cloudTTSInfo||!this._cloudOptions)return"";const e=this.getLanguages(this._cloudTTSInfo),t=this._cloudOptions,i=this.getSupportedGenders(t[0],this._cloudTTSInfo,this.hass.localize);return o`
      <div class="cloud-options">
        <ha-select
          fixedMenuPosition
          naturalMenuWidth
          .label=${this.hass.localize("ui.components.media-browser.tts.language")}
          .value=${t[0]}
          @selected=${this._handleLanguageChange}
          @closed=${j}
        >
          ${e.map((([e,t])=>o`<mwc-list-item .value=${e}>${t}</mwc-list-item>`))}
        </ha-select>

        <ha-select
          fixedMenuPosition
          naturalMenuWidth
          .label=${this.hass.localize("ui.components.media-browser.tts.gender")}
          .value=${t[1]}
          @selected=${this._handleGenderChange}
          @closed=${j}
        >
          ${i.map((([e,t])=>o`<mwc-list-item .value=${e}>${t}</mwc-list-item>`))}
        </ha-select>
      </div>
    `}},{kind:"method",key:"willUpdate",value:function(e){var t,a;if(n(r(i.prototype),"willUpdate",this).call(this,e),e.has("item")){if(this.item.media_content_id){const e=new URLSearchParams(this.item.media_content_id.split("?")[1]),t=e.get("message"),i=e.get("language"),a=e.get("gender");t&&(this._message=t),i&&a&&(this._cloudOptions=[i,a])}this.isCloudItem&&!this._cloudTTSInfo&&((a=this.hass,a.callWS({type:"cloud/tts/info"})).then((e=>{this._cloudTTSInfo=e})),(e=>e.callWS({type:"cloud/status"}))(this.hass).then((e=>{e.logged_in&&(this._cloudDefaultOptions=e.prefs.tts_default_voice,this._cloudOptions||(this._cloudOptions={...this._cloudDefaultOptions}))})))}if(e.has("message"))return;const s=null===(t=this.shadowRoot.querySelector("ha-textarea"))||void 0===t?void 0:t.value;void 0!==s&&s!==this._message&&(this._message=s)}},{kind:"method",key:"_handleLanguageChange",value:async function(e){e.target.value!==this._cloudOptions[0]&&(this._cloudOptions=[e.target.value,this._cloudOptions[1]])}},{kind:"method",key:"_handleGenderChange",value:async function(e){e.target.value!==this._cloudOptions[1]&&(this._cloudOptions=[this._cloudOptions[0],e.target.value])}},{kind:"field",key:"getLanguages",value:()=>d(G)},{kind:"field",key:"getSupportedGenders",value:()=>d(J)},{kind:"get",key:"isCloudItem",value:function(){return this.item.media_content_id.startsWith("media-source://tts/cloud")}},{kind:"method",key:"_ttsClicked",value:async function(){const e=this.shadowRoot.querySelector("ha-textarea").value;this._message=e;const t={...this.item},i=new URLSearchParams;i.append("message",e),this._cloudOptions&&(i.append("language",this._cloudOptions[0]),i.append("gender",this._cloudOptions[1])),t.media_content_id=`${t.media_content_id.split("?")[0]}?${i.toString()}`,t.can_play=!0,t.title=e,l(this,"tts-picked",{item:t})}},{kind:"method",key:"_storeDefaults",value:async function(){const e=this._cloudDefaultOptions;this._cloudDefaultOptions=[...this._cloudOptions];try{await(t=this.hass,i={tts_default_voice:this._cloudDefaultOptions},t.callWS({type:"cloud/update_prefs",...i}))}catch(t){this._cloudDefaultOptions=e,P(this,{text:this.hass.localize("ui.components.media-browser.tts.faild_to_store_defaults",{error:t.message||t})})}var t,i}},{kind:"field",static:!0,key:"styles",value:()=>[c,h`
      :host {
        margin: 16px auto;
        padding: 0 8px;
        display: flex;
        flex-direction: column;
        max-width: 400px;
      }
      .cloud-options {
        margin-top: 16px;
        display: flex;
        justify-content: space-between;
      }
      .cloud-options ha-select {
        width: 48%;
      }
      ha-textarea {
        width: 100%;
      }
      button.link {
        color: var(--primary-color);
      }
      .card-actions {
        display: flex;
        justify-content: space-between;
      }
    `]}]}}),i),t([m("ha-media-player-browse")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"entityId",value:void 0},{kind:"field",decorators:[a()],key:"action",value:()=>"play"},{kind:"field",decorators:[a({type:Boolean})],key:"dialog",value:()=>!1},{kind:"field",decorators:[a()],key:"navigateIds",value:void 0},{kind:"field",decorators:[a({type:Boolean,attribute:"narrow",reflect:!0})],key:"_narrow",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,attribute:"scroll",reflect:!0})],key:"_scrolled",value:()=>!1},{kind:"field",decorators:[s()],key:"_error",value:void 0},{kind:"field",decorators:[s()],key:"_parentItem",value:void 0},{kind:"field",decorators:[s()],key:"_currentItem",value:void 0},{kind:"field",decorators:[u(".header")],key:"_header",value:void 0},{kind:"field",decorators:[u(".content")],key:"_content",value:void 0},{kind:"field",decorators:[z(".lazythumbnail")],key:"_thumbnails",value:void 0},{kind:"field",key:"_headerOffsetHeight",value:()=>0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"field",key:"_intersectionObserver",value:void 0},{kind:"method",key:"connectedCallback",value:function(){n(r(i.prototype),"connectedCallback",this).call(this),this.updateComplete.then((()=>this._attachResizeObserver()))}},{kind:"method",key:"disconnectedCallback",value:function(){this._resizeObserver&&this._resizeObserver.disconnect(),this._intersectionObserver&&this._intersectionObserver.disconnect()}},{kind:"method",key:"refresh",value:async function(){const e=this.navigateIds[this.navigateIds.length-1];try{this._currentItem=await this._fetchData(this.entityId,e.media_content_id,e.media_content_type),l(this,"media-browsed",{ids:this.navigateIds,current:this._currentItem})}catch(e){this._setError(e)}}},{kind:"method",key:"play",value:function(){var e;null!==(e=this._currentItem)&&void 0!==e&&e.can_play&&this._runAction(this._currentItem)}},{kind:"method",key:"render",value:function(){if(this._error)return o`
        <div class="container">${this._renderError(this._error)}</div>
      `;if(!this._currentItem)return o`<ha-circular-progress active></ha-circular-progress>`;const e=this._currentItem,t=this.hass.localize(`ui.components.media-browser.class.${e.media_class}`),i=e.children||[],a=O[e.media_class],s=e.children_media_class?O[e.children_media_class]:O.directory;return o`
              ${e.can_play?o` <div
                      class="header ${p({"no-img":!e.thumbnail,"no-dialog":!this.dialog})}"
                      @transitionend=${this._setHeaderHeight}
                    >
                      <div class="header-content">
                        ${e.thumbnail?o`
                              <div
                                class="img"
                                style=${g({backgroundImage:e.thumbnail?`url(${e.thumbnail})`:"none"})}
                              >
                                ${this._narrow&&null!=e&&e.can_play?o`
                                      <ha-fab
                                        mini
                                        .item=${e}
                                        @click=${this._actionClicked}
                                      >
                                        <ha-svg-icon
                                          slot="icon"
                                          .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                          .path=${"play"===this.action?_:v}
                                        ></ha-svg-icon>
                                        ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                                      </ha-fab>
                                    `:""}
                              </div>
                            `:o``}
                        <div class="header-info">
                          <div class="breadcrumb">
                            <h1 class="title">${e.title}</h1>
                            ${t?o` <h2 class="subtitle">${t}</h2> `:""}
                          </div>
                          ${!e.can_play||e.thumbnail&&this._narrow?"":o`
                                <mwc-button
                                  raised
                                  .item=${e}
                                  @click=${this._actionClicked}
                                >
                                  <ha-svg-icon
                                    .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                    .path=${"play"===this.action?_:v}
                                  ></ha-svg-icon>
                                  ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                                </mwc-button>
                              `}
                        </div>
                      </div>
                    </div>`:""}
          <div
            class="content"
            @scroll=${this._scroll}
            @touchmove=${this._scroll}
          >
            ${this._error?o`
                    <div class="container">
                      ${this._renderError(this._error)}
                    </div>
                  `:(n=e.media_content_id,n.startsWith("media-source://tts/")?o`
                    <ha-browse-media-tts
                      .item=${e}
                      .hass=${this.hass}
                      .action=${this.action}
                      @tts-picked=${this._ttsPicked}
                    ></ha-browse-media-tts>
                  `:i.length||e.not_shown?"grid"===s.layout?o`
                    <div
                      class="children ${p({portrait:"portrait"===s.thumbnail_ratio})}"
                    >
                      ${i.map((e=>o`
                          <div
                            class="child"
                            .item=${e}
                            @click=${this._childClicked}
                          >
                            <ha-card outlined>
                              <div class="thumbnail">
                                ${e.thumbnail?o`
                                      <div
                                        class="${["app","directory"].includes(e.media_class)?"centered-image":""} image lazythumbnail"
                                        data-src=${e.thumbnail}
                                      ></div>
                                    `:o`
                                      <div class="icon-holder image">
                                        <ha-svg-icon
                                          class="folder"
                                          .path=${O["directory"===e.media_class&&e.children_media_class||e.media_class].icon}
                                        ></ha-svg-icon>
                                      </div>
                                    `}
                                ${e.can_play?o`
                                      <ha-icon-button
                                        class="play ${p({can_expand:e.can_expand})}"
                                        .item=${e}
                                        .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                        .path=${"play"===this.action?_:v}
                                        @click=${this._actionClicked}
                                      ></ha-icon-button>
                                    `:""}
                              </div>
                              <div class="title">
                                ${e.title}
                                <paper-tooltip
                                  fitToVisibleBounds
                                  position="top"
                                  offset="4"
                                  >${e.title}</paper-tooltip
                                >
                              </div>
                            </ha-card>
                          </div>
                        `))}
                      ${e.not_shown?o`
                            <div class="grid not-shown">
                              <div class="title">
                                ${this.hass.localize("ui.components.media-browser.not_shown",{count:e.not_shown})}
                              </div>
                            </div>
                          `:""}
                    </div>
                  `:o`
                    <mwc-list>
                      ${i.map((e=>o`
                          <mwc-list-item
                            @click=${this._childClicked}
                            .item=${e}
                            .graphic=${a.show_list_images?"medium":"avatar"}
                            dir=${A(this.hass)}
                          >
                            <div
                              class=${p({graphic:!0,lazythumbnail:!0===a.show_list_images})}
                              data-src=${f(a.show_list_images&&e.thumbnail?e.thumbnail:void 0)}
                              slot="graphic"
                            >
                              <ha-icon-button
                                class="play ${p({show:!a.show_list_images||!e.thumbnail})}"
                                .item=${e}
                                .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                .path=${"play"===this.action?_:v}
                                @click=${this._actionClicked}
                              ></ha-icon-button>
                            </div>
                            <span class="title">${e.title}</span>
                          </mwc-list-item>
                          <li divider role="separator"></li>
                        `))}
                      ${e.not_shown?o`
                            <mwc-list-item
                              noninteractive
                              class="not-shown"
                              .graphic=${a.show_list_images?"medium":"avatar"}
                              dir=${A(this.hass)}
                            >
                              <span class="title">
                                ${this.hass.localize("ui.components.media-browser.not_shown",{count:e.not_shown})}
                              </span>
                            </mwc-list-item>
                          `:""}
                    </mwc-list>
                  `:o`
                    <div class="container no-items">
                      ${"media-source://media_source/local/."===e.media_content_id?o`
                            <div class="highlight-add-button">
                              <span>
                                <ha-svg-icon
                                  .path=${b}
                                ></ha-svg-icon>
                              </span>
                              <span>
                                ${this.hass.localize("ui.components.media-browser.file_management.highlight_button")}
                              </span>
                            </div>
                          `:this.hass.localize("ui.components.media-browser.no_items")}
                    </div>
                  `)}
          </div>
        </div>
      </div>
    `;var n}},{kind:"method",key:"firstUpdated",value:function(){this._measureCard(),this._attachResizeObserver()}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.size>1||!e.has("hass"))return!0;const t=e.get("hass");return void 0===t||t.localize!==this.hass.localize}},{kind:"method",key:"willUpdate",value:function(e){var t;if(n(r(i.prototype),"willUpdate",this).call(this,e),e.has("entityId"))this._setError(void 0);else if(!e.has("navigateIds"))return;this._setError(void 0);const a=e.get("navigateIds"),s=this.navigateIds;null===(t=this._content)||void 0===t||t.scrollTo(0,0),this._scrolled=!1;const o=this._currentItem,d=this._parentItem;this._currentItem=void 0,this._parentItem=void 0;const c=s[s.length-1],h=s.length>1?s[s.length-2]:void 0;let m,u;e.has("entityId")||(a&&s.length===a.length+1&&a.every(((e,t)=>{const i=s[t];return i.media_content_id===e.media_content_id&&i.media_content_type===e.media_content_type}))?u=Promise.resolve(o):a&&s.length===a.length-1&&s.every(((e,t)=>{const i=a[t];return e.media_content_id===i.media_content_id&&e.media_content_type===i.media_content_type}))&&(m=Promise.resolve(d))),m||(m=this._fetchData(this.entityId,c.media_content_id,c.media_content_type)),m.then((e=>{this._currentItem=e,l(this,"media-browsed",{ids:s,current:e})}),(t=>{a&&e.has("entityId")&&s.length===a.length&&a.every(((e,t)=>s[t].media_content_id===e.media_content_id&&s[t].media_content_type===e.media_content_type))?l(this,"media-browsed",{ids:[{media_content_id:void 0,media_content_type:void 0}],replace:!0}):this._setError(t)})),u||void 0===h||(u=this._fetchData(this.entityId,h.media_content_id,h.media_content_type)),u&&u.then((e=>{this._parentItem=e}))}},{kind:"method",key:"updated",value:function(e){n(r(i.prototype),"updated",this).call(this,e),e.has("_scrolled")?this._animateHeaderHeight():e.has("_currentItem")&&(this._setHeaderHeight(),this._attachIntersectionObserver())}},{kind:"method",key:"_actionClicked",value:function(e){e.stopPropagation();const t=e.currentTarget.item;this._runAction(t)}},{kind:"method",key:"_runAction",value:function(e){l(this,"media-picked",{item:e,navigateIds:this.navigateIds})}},{kind:"method",key:"_ttsPicked",value:function(e){e.stopPropagation();const t=this.navigateIds.slice(0,-1);t.push(e.detail.item),l(this,"media-picked",{...e.detail,navigateIds:t})}},{kind:"method",key:"_childClicked",value:async function(e){const t=e.currentTarget.item;t&&(t.can_expand?l(this,"media-browsed",{ids:[...this.navigateIds,t]}):this._runAction(t))}},{kind:"method",key:"_fetchData",value:async function(e,t,i){return e!==C?S(this.hass,e,t,i):V(this.hass,t)}},{kind:"method",key:"_measureCard",value:function(){this._narrow=(this.dialog?window.innerWidth:this.offsetWidth)<450}},{kind:"method",key:"_attachResizeObserver",value:async function(){this._resizeObserver||(await D(),this._resizeObserver=new ResizeObserver(E((()=>this._measureCard()),250,!1))),this._resizeObserver.observe(this)}},{kind:"method",key:"_attachIntersectionObserver",value:async function(){if(!("IntersectionObserver"in window)||!this._thumbnails)return;this._intersectionObserver||(this._intersectionObserver=new IntersectionObserver((async(e,t)=>{await Promise.all(e.map((async e=>{if(!e.isIntersecting)return;const i=e.target;let a=i.dataset.src;if(a){if(a.startsWith("/")){a=(await T(this.hass,a)).path}else if(a.startsWith("https://brands.home-assistant.io")){var s;a=W({domain:L(a),type:"icon",useFallback:!0,darkOptimized:null===(s=this.hass.themes)||void 0===s?void 0:s.darkMode})}i.style.backgroundImage=`url(${a})`,t.unobserve(i)}})))})));const e=this._intersectionObserver;for(const t of this._thumbnails)e.observe(t)}},{kind:"method",key:"_closeDialogAction",value:function(){l(this,"close-dialog")}},{kind:"method",key:"_setError",value:function(e){this.dialog?e&&(this._closeDialogAction(),P(this,{title:this.hass.localize("ui.components.media-browser.media_browsing_error"),text:this._renderError(e)})):this._error=e}},{kind:"method",key:"_renderError",value:function(e){return"Media directory does not exist."===e.message?o`
        <h2>
          ${this.hass.localize("ui.components.media-browser.no_local_media_found")}
        </h2>
        <p>
          ${this.hass.localize("ui.components.media-browser.no_media_folder")}
          <br />
          ${this.hass.localize("ui.components.media-browser.setup_local_help","documentation",o`<a
              href=${U(this.hass,"/more-info/local-media/setup-media")}
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.components.media-browser.documentation")}</a
            >`)}
          <br />
          ${this.hass.localize("ui.components.media-browser.local_media_files")}
        </p>
      `:o`<span class="error">${e.message}</span>`}},{kind:"method",key:"_setHeaderHeight",value:async function(){await this.updateComplete;const e=this._header,t=this._content;e&&t&&(this._headerOffsetHeight=e.offsetHeight,t.style.marginTop=`${this._headerOffsetHeight}px`,t.style.maxHeight=`calc(var(--media-browser-max-height, 100%) - ${this._headerOffsetHeight}px)`)}},{kind:"method",key:"_animateHeaderHeight",value:function(){let e;const t=i=>{void 0===e&&(e=i);const a=i-e;this._setHeaderHeight(),a<400&&requestAnimationFrame(t)};requestAnimationFrame(t)}},{kind:"method",decorators:[y({passive:!0})],key:"_scroll",value:function(e){const t=e.currentTarget;!this._scrolled&&t.scrollTop>this._headerOffsetHeight?this._scrolled=!0:this._scrolled&&t.scrollTop<this._headerOffsetHeight&&(this._scrolled=!1)}},{kind:"get",static:!0,key:"styles",value:function(){return[k,h`
        :host {
          display: flex;
          flex-direction: column;
          position: relative;
        }

        ha-circular-progress {
          --mdc-theme-primary: var(--primary-color);
          display: flex;
          justify-content: center;
          margin: 40px;
        }

        .container {
          padding: 16px;
        }

        .no-items {
          padding-left: 32px;
        }

        .highlight-add-button {
          display: flex;
          flex-direction: row-reverse;
          margin-right: 48px;
        }

        .highlight-add-button ha-svg-icon {
          position: relative;
          top: -0.5em;
          margin-left: 8px;
        }

        .content {
          overflow-y: auto;
          box-sizing: border-box;
        }

        /* HEADER */

        .header {
          display: flex;
          justify-content: space-between;
          border-bottom: 1px solid var(--divider-color);
          background-color: var(--card-background-color);
          position: absolute;
          top: 0;
          right: 0;
          left: 0;
          z-index: 5;
          padding: 16px;
        }
        .header_button {
          position: relative;
          right: -8px;
        }
        .header-content {
          display: flex;
          flex-wrap: wrap;
          flex-grow: 1;
          align-items: flex-start;
        }
        .header-content .img {
          height: 175px;
          width: 175px;
          margin-right: 16px;
          background-size: cover;
          border-radius: 2px;
          transition: width 0.4s, height 0.4s;
        }
        .header-info {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          align-self: stretch;
          min-width: 0;
          flex: 1;
        }
        .header-info mwc-button {
          display: block;
          --mdc-theme-primary: var(--primary-color);
          padding-bottom: 16px;
        }
        .breadcrumb {
          display: flex;
          flex-direction: column;
          overflow: hidden;
          flex-grow: 1;
          padding-top: 16px;
        }
        .breadcrumb .title {
          font-size: 32px;
          line-height: 1.2;
          font-weight: bold;
          margin: 0;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          padding-right: 8px;
        }
        .breadcrumb .previous-title {
          font-size: 14px;
          padding-bottom: 8px;
          color: var(--secondary-text-color);
          overflow: hidden;
          text-overflow: ellipsis;
          cursor: pointer;
          --mdc-icon-size: 14px;
        }
        .breadcrumb .subtitle {
          font-size: 16px;
          overflow: hidden;
          text-overflow: ellipsis;
          margin-bottom: 0;
          transition: height 0.5s, margin 0.5s;
        }

        .not-shown {
          font-style: italic;
          color: var(--secondary-text-color);
        }

        .grid.not-shown {
          display: flex;
          align-items: center;
          text-align: center;
        }

        /* ============= CHILDREN ============= */

        mwc-list {
          --mdc-list-vertical-padding: 0;
          --mdc-list-item-graphic-margin: 0;
          --mdc-theme-text-icon-on-background: var(--secondary-text-color);
          margin-top: 10px;
        }

        mwc-list li:last-child {
          display: none;
        }

        mwc-list li[divider] {
          border-bottom-color: var(--divider-color);
        }

        .children {
          display: grid;
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.1fr)
          );
          grid-gap: 16px;
          padding: 16px;
        }

        :host([dialog]) .children {
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.33fr)
          );
        }

        .child {
          display: flex;
          flex-direction: column;
          cursor: pointer;
        }

        ha-card {
          position: relative;
          width: 100%;
          box-sizing: border-box;
        }

        .children ha-card .thumbnail {
          width: 100%;
          position: relative;
          box-sizing: border-box;
          transition: padding-bottom 0.1s ease-out;
          padding-bottom: 100%;
        }

        .portrait.children ha-card .thumbnail {
          padding-bottom: 150%;
        }

        ha-card .image {
          border-radius: 3px 3px 0 0;
        }

        .image {
          position: absolute;
          top: 0;
          right: 0;
          left: 0;
          bottom: 0;
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center;
        }

        .centered-image {
          margin: 0 8px;
          background-size: contain;
        }

        .children ha-card .icon-holder {
          display: flex;
          justify-content: center;
          align-items: center;
        }

        .child .folder {
          color: var(--secondary-text-color);
          --mdc-icon-size: calc(var(--media-browse-item-size, 175px) * 0.4);
        }

        .child .play {
          position: absolute;
          transition: color 0.5s;
          border-radius: 50%;
          top: calc(50% - 50px);
          right: calc(50% - 35px);
          opacity: 0;
          transition: opacity 0.1s ease-out;
        }

        .child .play:not(.can_expand) {
          --mdc-icon-button-size: 70px;
          --mdc-icon-size: 48px;
        }

        ha-card:hover .play {
          opacity: 1;
        }

        ha-card:hover .play:not(.can_expand) {
          color: var(--primary-color);
        }

        ha-card:hover .play.can_expand {
          bottom: 8px;
        }

        .child .play.can_expand {
          background-color: rgba(var(--rgb-card-background-color), 0.5);
          top: auto;
          bottom: 0px;
          right: 8px;
          transition: bottom 0.1s ease-out, opacity 0.1s ease-out;
        }

        .child .play:hover {
          color: var(--primary-color);
        }

        ha-card:hover .lazythumbnail {
          opacity: 0.5;
        }

        .child .title {
          font-size: 16px;
          padding-top: 16px;
          padding-left: 2px;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 1;
          text-overflow: ellipsis;
        }

        .child ha-card .title {
          margin-bottom: 16px;
          padding-left: 16px;
        }

        mwc-list-item .graphic {
          background-size: contain;
          border-radius: 2px;
          display: flex;
          align-content: center;
          align-items: center;
          line-height: initial;
        }

        mwc-list-item .graphic .play {
          opacity: 0;
          transition: all 0.5s;
          background-color: rgba(var(--rgb-card-background-color), 0.5);
          border-radius: 50%;
          --mdc-icon-button-size: 40px;
        }

        mwc-list-item:hover .graphic .play {
          opacity: 1;
          color: var(--primary-text-color);
        }

        mwc-list-item .graphic .play.show {
          opacity: 1;
          background-color: transparent;
        }

        mwc-list-item .title {
          margin-left: 16px;
        }
        mwc-list-item[dir="rtl"] .title {
          margin-right: 16px;
          margin-left: 0;
        }

        /* ============= Narrow ============= */

        :host([narrow]) {
          padding: 0;
        }

        :host([narrow]) .media-source {
          padding: 0 24px;
        }

        :host([narrow]) .children {
          grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        }

        :host([narrow]) .breadcrumb .title {
          font-size: 24px;
        }
        :host([narrow]) .header {
          padding: 0;
        }
        :host([narrow]) .header.no-dialog {
          display: block;
        }
        :host([narrow]) .header_button {
          position: absolute;
          top: 14px;
          right: 8px;
        }
        :host([narrow]) .header-content {
          flex-direction: column;
          flex-wrap: nowrap;
        }
        :host([narrow]) .header-content .img {
          height: auto;
          width: 100%;
          margin-right: 0;
          padding-bottom: 50%;
          margin-bottom: 8px;
          position: relative;
          background-position: center;
          border-radius: 0;
          transition: width 0.4s, height 0.4s, padding-bottom 0.4s;
        }
        ha-fab {
          position: absolute;
          --mdc-theme-secondary: var(--primary-color);
          bottom: -20px;
          right: 20px;
        }
        :host([narrow]) .header-info mwc-button {
          margin-top: 16px;
          margin-bottom: 8px;
        }
        :host([narrow]) .header-info {
          padding: 0 16px 8px;
        }

        /* ============= Scroll ============= */
        :host([scroll]) .breadcrumb .subtitle {
          height: 0;
          margin: 0;
        }
        :host([scroll]) .breadcrumb .title {
          -webkit-line-clamp: 1;
        }
        :host(:not([narrow])[scroll]) .header:not(.no-img) ha-icon-button {
          align-self: center;
        }
        :host([scroll]) .header-info mwc-button,
        .no-img .header-info mwc-button {
          padding-right: 4px;
        }
        :host([scroll][narrow]) .no-img .header-info mwc-button {
          padding-right: 16px;
        }
        :host([scroll]) .header-info {
          flex-direction: row;
        }
        :host([scroll]) .header-info mwc-button {
          align-self: center;
          margin-top: 0;
          margin-bottom: 0;
          padding-bottom: 0;
        }
        :host([scroll][narrow]) .no-img .header-info {
          flex-direction: row-reverse;
        }
        :host([scroll][narrow]) .header-info {
          padding: 20px 24px 10px 24px;
          align-items: center;
        }
        :host([scroll]) .header-content {
          align-items: flex-end;
          flex-direction: row;
        }
        :host([scroll]) .header-content .img {
          height: 75px;
          width: 75px;
        }
        :host([scroll]) .breadcrumb {
          padding-top: 0;
          align-self: center;
        }
        :host([scroll][narrow]) .header-content .img {
          height: 100px;
          width: 100px;
          padding-bottom: initial;
          margin-bottom: 0;
        }
        :host([scroll]) ha-fab {
          bottom: 0px;
          right: -24px;
          --mdc-fab-box-shadow: none;
          --mdc-theme-secondary: rgba(var(--rgb-primary-color), 0.5);
        }
      `]}}]}}),i);t([m("ha-media-manage-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"currentItem",value:void 0},{kind:"field",decorators:[s()],key:"_uploading",value:()=>0},{kind:"method",key:"render",value:function(){return this.currentItem&&M(this.currentItem.media_content_id||"")?o`
      <mwc-button
        .label=${this.hass.localize("ui.components.media-browser.file_management.manage")}
        @click=${this._manage}
      >
        <ha-svg-icon .path=${w} slot="icon"></ha-svg-icon>
      </mwc-button>
    `:o``}},{kind:"method",key:"_manage",value:function(){var e,t;e=this,t={currentItem:this.currentItem,onClose:()=>l(this,"media-refresh")},l(e,"show-dialog",{dialogTag:"dialog-media-manage",dialogImport:()=>import("./c.96d13fc4.js"),dialogParams:t})}},{kind:"field",static:!0,key:"styles",value:()=>h`
    mwc-button {
      /* We use icon + text to show disabled state */
      --mdc-button-disabled-ink-color: --mdc-theme-primary;
    }

    ha-svg-icon[slot="icon"],
    ha-circular-progress[slot="icon"] {
      vertical-align: middle;
    }
  `}]}}),i),t([m("dialog-media-player-browse")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_currentItem",value:void 0},{kind:"field",decorators:[s()],key:"_navigateIds",value:void 0},{kind:"field",decorators:[s()],key:"_params",value:void 0},{kind:"field",decorators:[u("ha-media-player-browse")],key:"_browser",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._navigateIds=e.navigateIds||[{media_content_id:void 0,media_content_type:void 0}]}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._navigateIds=void 0,this._currentItem=void 0,l(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params&&this._navigateIds?o`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        hideActions
        flexContent
        .heading=${this._currentItem?this._currentItem.title:this.hass.localize("ui.components.media-browser.media-player-browser")}
        @closed=${this.closeDialog}
      >
        <ha-header-bar slot="heading">
          ${this._navigateIds.length>1?o`
                <ha-icon-button
                  slot="navigationIcon"
                  .path=${x}
                  @click=${this._goBack}
                ></ha-icon-button>
              `:""}
          <span slot="title">
            ${this._currentItem?this._currentItem.title:this.hass.localize("ui.components.media-browser.media-player-browser")}
          </span>

          <ha-media-manage-button
            slot="actionItems"
            .hass=${this.hass}
            .currentItem=${this._currentItem}
            @media-refresh=${this._refreshMedia}
          ></ha-media-manage-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.dialogs.generic.close")}
            .path=${$}
            dialogAction="close"
            slot="actionItems"
            class="header_button"
            dir=${A(this.hass)}
          ></ha-icon-button>
        </ha-header-bar>
        <ha-media-player-browse
          dialog
          .hass=${this.hass}
          .entityId=${this._params.entityId}
          .navigateIds=${this._navigateIds}
          .action=${this._action}
          @close-dialog=${this.closeDialog}
          @media-picked=${this._mediaPicked}
          @media-browsed=${this._mediaBrowsed}
        ></ha-media-player-browse>
      </ha-dialog>
    `:o``}},{kind:"method",key:"_goBack",value:function(){var e;this._navigateIds=null===(e=this._navigateIds)||void 0===e?void 0:e.slice(0,-1),this._currentItem=void 0}},{kind:"method",key:"_mediaBrowsed",value:function(e){this._navigateIds=e.detail.ids,this._currentItem=e.detail.current}},{kind:"method",key:"_mediaPicked",value:function(e){this._params.mediaPickedCallback(e.detail),"play"!==this._action&&this.closeDialog()}},{kind:"get",key:"_action",value:function(){return this._params.action||"play"}},{kind:"method",key:"_refreshMedia",value:function(){this._browser.refresh()}},{kind:"get",static:!0,key:"styles",value:function(){return[I,h`
        ha-dialog {
          --dialog-z-index: 8;
          --dialog-content-padding: 0;
        }

        ha-media-player-browse {
          --media-browser-max-height: calc(100vh - 65px);
        }

        @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --dialog-surface-position: fixed;
            --dialog-surface-top: 40px;
            --mdc-dialog-max-height: calc(100vh - 72px);
          }
          ha-media-player-browse {
            position: initial;
            --media-browser-max-height: 100vh - 137px;
            width: 700px;
          }
        }

        ha-header-bar {
          --mdc-theme-on-primary: var(--primary-text-color);
          --mdc-theme-primary: var(--mdc-theme-surface);
          flex-shrink: 0;
          border-bottom: 1px solid var(--divider-color, rgba(0, 0, 0, 0.12));
        }

        ha-media-manage-button {
          --mdc-theme-primary: var(--mdc-theme-on-primary);
        }
      `]}}]}}),i);var Q=Object.freeze({__proto__:null});export{V as b,Q as d,M as i,N as r,R as u};
