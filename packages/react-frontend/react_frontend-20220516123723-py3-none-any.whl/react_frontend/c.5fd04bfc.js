import{ar as e,_ as t,s as r,e as a,$ as i,n as o,t as s,dv as d,aq as n,f as c,dH as h,dI as l,Z as u,dJ as v,cD as k,dK as p,dL as g,dd as f,g as b,i as _,ap as $,dM as y,dN as m,r as x,dO as w,dP as N,dQ as I,dR as T,h as S}from"./main-ac83c92b.js";import{Q as O,a8 as j,k as E}from"./c.027db416.js";import{d as B}from"./c.d6711a1d.js";import"./c.622dfac1.js";import{e as F}from"./c.8d0ef0b0.js";const P=e`
  .tabs {
    background-color: var(--primary-background-color);
    border-top: 1px solid var(--divider-color);
    border-bottom: 1px solid var(--divider-color);
    display: flex;
    padding-left: 4px;
  }

  .tabs.top {
    border-top: none;
  }

  .tabs > * {
    padding: 2px 16px;
    cursor: pointer;
    position: relative;
    bottom: -1px;
    border: none;
    border-bottom: 2px solid transparent;
    user-select: none;
    background: none;
    color: var(--primary-text-color);
    outline: none;
    transition: background 15ms linear;
  }

  .tabs > *.active {
    border-bottom-color: var(--accent-color);
  }

  .tabs > *:focus,
  .tabs > *:hover {
    background: var(--secondary-background-color);
  }
`;t([o("ha-trace-config")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"trace",value:void 0},{kind:"method",key:"render",value:function(){return i`
      <ha-code-editor
        .value=${B(this.trace.config).trimRight()}
        readOnly
        dir="ltr"
      ></ha-code-editor>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[e``]}}]}}),r);t([o("hat-graph-branch")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"selected",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"start",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"short",value:()=>!1},{kind:"field",decorators:[s()],key:"_branches",value:()=>[]},{kind:"field",key:"_totalWidth",value:()=>0},{kind:"field",key:"_maxHeight",value:()=>0},{kind:"method",key:"_updateBranches",value:function(e){let t=0;const r=[],a=[];e.target.assignedElements().forEach((e=>{const i=e.clientWidth,o=e.clientHeight;a.push({x:i/2+t,height:o,start:e.hasAttribute("graphStart"),end:e.hasAttribute("graphEnd"),track:e.hasAttribute("track")}),t+=i,r.push(o)})),this._totalWidth=t,this._maxHeight=Math.max(...r),this._branches=a.sort(((e,t)=>e.track&&!t.track?1:e.track&&t.track?0:-1))}},{kind:"method",key:"render",value:function(){return i`
      <slot name="head"></slot>
      ${this.start?"":d`
            <svg
              id="top"
              width="${this._totalWidth}"
            >
              ${this._branches.map((e=>e.start?"":d`
                  <path
                    class=${n({track:e.track})}
                    d="
                      M ${this._totalWidth/2} 0
                      L ${e.x} ${20}
                      "/>
                `))}
            </svg>
          `}
      <div id="branches">
        <svg id="lines" width=${this._totalWidth} height=${this._maxHeight}>
          ${this._branches.map((e=>e.end?"":d`
                    <path
                      class=${n({track:e.track})}
                      d="
                        M ${e.x} ${e.height}
                        v ${this._maxHeight-e.height}
                        "/>
                  `))}
        </svg>
        <slot @slotchange=${this._updateBranches}></slot>
      </div>

      ${this.short?"":d`
            <svg
              id="bottom"
              width="${this._totalWidth}"
            >
              ${this._branches.map((e=>e.end?"":d`
                  <path
                    class=${n({track:e.track})}
                    d="
                      M ${e.x} 0
                      V ${10}
                      L ${this._totalWidth/2} ${30}
                      "/>
                `))}
            </svg>
          `}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      :host {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      :host(:focus) {
        outline: none;
      }
      #branches {
        position: relative;
        display: flex;
        flex-direction: row;
        align-items: start;
      }
      ::slotted(*) {
        z-index: 1;
      }
      ::slotted([slot="head"]) {
        margin-bottom: calc(var(--hat-graph-branch-height) / -2);
      }
      #lines {
        position: absolute;
      }
      #top {
        height: var(--hat-graph-branch-height);
      }
      #bottom {
        height: calc(var(--hat-graph-branch-height) + var(--hat-graph-spacing));
      }
      path {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
      path.track {
        stroke: var(--track-clr);
      }
      :host([disabled]) path {
        stroke: var(--disabled-clr);
      }
    `}}]}}),r),t([o("hat-graph-node")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a()],key:"iconPath",value:void 0},{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"graphStart",value:void 0},{kind:"field",decorators:[a({type:Boolean,attribute:"nofocus"})],key:"noFocus",value:()=>!1},{kind:"field",decorators:[a({reflect:!0,type:Number})],key:"badge",value:void 0},{kind:"method",key:"updated",value:function(e){e.has("noFocus")&&(this.hasAttribute("tabindex")||this.noFocus?void 0!==e.get("noFocus")&&this.noFocus&&this.removeAttribute("tabindex"):this.setAttribute("tabindex","0"))}},{kind:"method",key:"render",value:function(){const e=30+(this.graphStart?2:11);return i`
      <svg
        width="${40}px"
        height="${e}px"
        viewBox="-${Math.ceil(20)} -${this.graphStart?Math.ceil(e/2):Math.ceil(25)} ${40} ${e}"
      >
        ${this.graphStart?"":d`
          <path
            class="connector"
            d="
              M 0 ${-25}
              L 0 0
            "
            line-caps="round"
          />
          `}
        <g class="node">
          <circle cx="0" cy="0" r=${15} />
          }
          ${this.badge?d`
        <g class="number">
          <circle
            cx="8"
            cy=${-15}
            r="8"
          ></circle>
          <text
            x="8"
            y=${-15}
            text-anchor="middle"
            alignment-baseline="middle"
          >${this.badge>9?"9+":this.badge}</text>
        </g>
      `:""}
          <g style="pointer-events: none" transform="translate(${-12} ${-12})">
            ${this.iconPath?d`<path class="icon" d=${this.iconPath}/>`:""}
          </g>
        </g>
      </svg>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      :host {
        display: flex;
        flex-direction: column;
        min-width: calc(var(--hat-graph-node-size) + var(--hat-graph-spacing));
        height: calc(
          var(--hat-graph-node-size) + var(--hat-graph-spacing) + 1px
        );
      }
      :host([graphStart]) {
        height: calc(var(--hat-graph-node-size) + 2px);
      }
      :host([track]) {
        --stroke-clr: var(--track-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host([active]) circle {
        --stroke-clr: var(--active-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host(:focus) {
        outline: none;
      }
      :host(:hover) circle {
        --stroke-clr: var(--hover-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host([disabled]) circle {
        stroke: var(--disabled-clr);
      }
      svg {
        width: 100%;
        height: 100%;
      }
      circle,
      path.connector {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
      circle {
        fill: var(--background-clr);
        stroke: var(--circle-clr, var(--stroke-clr));
      }
      .number circle {
        fill: var(--track-clr);
        stroke: none;
        stroke-width: 0;
      }
      .number text {
        font-size: smaller;
      }
      path.icon {
        fill: var(--icon-clr);
      }
    `}}]}}),r),t([o("hat-graph-spacer")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"method",key:"render",value:function(){return i`
      <svg viewBox="-${5} 0 10 ${41}">
        <path
          d="
              M 0 ${41}
              V 0
            "
          line-caps="round"
        />
        }
      </svg>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      :host {
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      svg {
        width: var(--hat-graph-spacing);
        height: calc(
          var(--hat-graph-spacing) + var(--hat-graph-node-size) + 1px
        );
      }
      :host([track]) {
        --stroke-clr: var(--track-clr);
      }
      :host-context([disabled]) {
        --stroke-clr: var(--disabled-clr);
      }
      path {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
    `}}]}}),r),t([o("react-script-graph")],(function(t,r){class o extends r{constructor(...e){super(...e),t(this)}}return{F:o,d:[{kind:"field",decorators:[a({attribute:!1})],key:"trace",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"selected",value:void 0},{kind:"field",key:"renderedNodes",value:()=>({})},{kind:"field",key:"trackedNodes",value:()=>({})},{kind:"method",key:"selectNode",value:function(e,t){return()=>{c(this,"graph-node-selected",{config:e,path:t})}}},{kind:"method",key:"render_actor",value:function(e,t){const r=`actor/${t}`,a=`${r}/trigger`,o=`${r}/condition`,s=this.trace&&a in this.trace.trace;this.renderedNodes[a]={config:e.trigger,path:a},s&&(this.trackedNodes[a]=this.renderedNodes[a]);const d=this.get_condition_info(o);return e.condition?i`
                <div ?track=${s&&d.track&&d.trackPass}>
                    ${this.render_actor_node(e,s,a)}
                    ${this.render_condition_node(e.condition,`${o}`,!1,!1===e.trigger.enabled)}
                </div>
            `:this.render_actor_node(e,s,a)}},{kind:"method",key:"render_actor_node",value:function(e,t,r){return i`
            <hat-graph-node
                graphStart
                ?track=${t}
                @focus=${this.selectNode(e,r)}
                ?active=${this.selected===r}
                .iconPath=${h}
                .notEnabled=${!1===e.trigger.enabled}
                tabindex=${t?"0":"-1"}
            ></hat-graph-node>`}},{kind:"method",key:"render_reactor",value:function(e,t,r=!1){const a=`reactor/${t}`,o=`${a}/event`,s=`${a}/condition`,d=this.trace&&o in this.trace.trace;this.renderedNodes[o]={config:e.event,path:o},d&&(this.trackedNodes[o]=this.renderedNodes[o]);const n=this.get_condition_info(s);return e.condition?i`
                <div ?track=${d||n.has_condition&&n.trackFailed}>
                    ${this.render_condition_node(e.condition,s,!1,!1===e.event.enabled)}
                    ${this.render_reactor_node(e,d,o,r)}
                </div>
            `:this.render_reactor_node(e,d,o,r)}},{kind:"method",key:"render_reactor_node",value:function(e,t,r,a){return i`
            <hat-graph-node
                .iconPath=${"immediate"===e.timing?l:u}
                @focus=${this.selectNode(e,r)}
                ?track=${t}
                ?active=${this.selected===r}
                .notEnabled=${a||!1===e.event.enabled}
                tabindex=${this.trace&&r in this.trace.trace?"0":"-1"}
                graphEnd 
            ></hat-graph-node>`}},{kind:"method",key:"render_condition_node",value:function(e,t,r=!1,a=!1){this.renderedNodes[t]={config:e,path:t},this.trace&&t in this.trace.trace&&(this.trackedNodes[t]=this.renderedNodes[t]);const o=this.get_condition_info(t);return i`
            <hat-graph-branch
                @focus=${this.selectNode(e,t)}
                ?track=${o.track}
                ?active=${this.selected===t}
                .notEnabled=${a||!1===e.enabled}
                tabindex=${void 0===o.trace?"-1":"0"}
                short
            >
                <hat-graph-node
                    .graphStart=${r}
                    slot="head"
                    ?track=${o.track}
                    ?active=${this.selected===t}
                    .notEnabled=${a||!1===e.enabled}
                    .iconPath=${v}
                    nofocus
                ></hat-graph-node>
                <div
                    style=${"width: 40px;"}
                    graphStart
                    graphEnd
                ></div>
                <div ?track=${o.trackPass}></div>
                <hat-graph-node
                    .iconPath=${k}
                    nofocus
                    ?track=${o.trackFailed}
                    ?active=${this.selected===t}
                    .notEnabled=${a||!1===e.enabled}
                ></hat-graph-node>
            </hat-graph-branch>
        `}},{kind:"method",key:"render_parallel_node",value:function(e,t,r=!1,a=!1){const o=this.trace&&t in this.trace.trace;this.renderedNodes[t]={config:e,path:t},o&&(this.trackedNodes[t]=this.renderedNodes[t]);const s=this.trace.trace[t];return i`
            <hat-graph-branch
                tabindex=${void 0===s?"-1":"0"}
                @focus=${this.selectNode(e,t)}
                ?track=${o}
                ?active=${this.selected===t}
                .notEnabled=${a}
                short
            >
                <hat-graph-node
                    .graphStart=${r}
                    .iconPath=${p}
                    ?track=${o}
                    ?active=${this.selected===t}
                    .notEnabled=${a}
                    slot="head"
                    nofocus
                ></hat-graph-node>
                ${F(this.trace.config.reactor).map(((e,t)=>this.render_reactor(e,t)))}
                
            </hat-graph-branch>
        `}},{kind:"method",key:"get_condition_info",value:function(e){const t=this.trace.trace[e];let r=!1,a=!1,i=!1,o=!1;if(t){a=!0;for(const e of t)if(e.result&&(r=!0,e.result.result?i=!0:o=!0),i&&o)break}return{trace:t,track:r,has_condition:a,trackPass:i,trackFailed:o}}},{kind:"method",key:"render",value:function(){const e=Object.keys(this.trackedNodes),t=F(this.trace.config.actor).map(((e,t)=>this.render_actor(e,t)));try{return i`
                <div class="parent graph-container">
                    ${i`
                        <hat-graph-branch start .short=${t.length<2}>
                            ${t}
                        </hat-graph-branch>`}
                    ${"parallel"in this.trace.config?i`
                            ${this.render_parallel_node(this.trace.config.parallel,"parallel",!1,!1)}`:i`
                            ${this.render_reactor(this.trace.config.reactor[0],0)}`}
                </div>
                <div class="actions">
                    <ha-icon-button
                        .disabled=${0===e.length||e[0]===this.selected}
                        @click=${this._previousTrackedNode}
                        .path=${g}
                    ></ha-icon-button>
                    <ha-icon-button
                        .disabled=${0===e.length||e[e.length-1]===this.selected}
                        @click=${this._nextTrackedNode}
                        .path=${f}
                    ></ha-icon-button>
                </div>
            `}catch(e){return i`
            <div class="error">
                Error rendering graph. Please download trace and share with the
                developers.
            </div>
        `}}},{kind:"method",key:"willUpdate",value:function(e){b(_(o.prototype),"willUpdate",this).call(this,e),e.has("trace")&&(this.renderedNodes={},this.trackedNodes={})}},{kind:"method",key:"updated",value:function(e){if(b(_(o.prototype),"updated",this).call(this,e),e.has("trace")){if(!this.selected||!(this.selected in this.trackedNodes)){const e=this.trackedNodes[Object.keys(this.trackedNodes)[0]];e&&c(this,"graph-node-selected",e)}if(this.trace){const e=Object.keys(this.trace.trace),t=Object.keys(this.renderedNodes).sort(((t,r)=>e.indexOf(t)-e.indexOf(r))),r={},a={};for(const e of t)a[e]=this.renderedNodes[e],e in this.trackedNodes&&(r[e]=this.trackedNodes[e]);this.renderedNodes=a,this.trackedNodes=r}}}},{kind:"method",key:"_previousTrackedNode",value:function(){const e=Object.keys(this.trackedNodes),t=e.indexOf(this.selected)-1;t>=0&&c(this,"graph-node-selected",this.trackedNodes[e[t]])}},{kind:"method",key:"_nextTrackedNode",value:function(){const e=Object.keys(this.trackedNodes),t=e.indexOf(this.selected)+1;t<e.length&&c(this,"graph-node-selected",this.trackedNodes[e[t]])}},{kind:"get",static:!0,key:"styles",value:function(){return e`
            :host {
                display: flex;
                --stroke-clr: var(--stroke-color, var(--secondary-text-color));
                --active-clr: var(--active-color, var(--primary-color));
                --track-clr: var(--track-color, var(--accent-color));
                --hover-clr: var(--hover-color, var(--primary-color));
                --disabled-clr: var(--disabled-color, var(--disabled-text-color));
                --disabled-active-clr: rgba(var(--rgb-primary-color), 0.5);
                --disabled-hover-clr: rgba(var(--rgb-primary-color), 0.7);
                --default-trigger-color: 3, 169, 244;
                --rgb-trigger-color: var(--trigger-color, var(--default-trigger-color));
                --background-clr: var(--background-color, white);
                --default-icon-clr: var(--icon-color, black);
                --icon-clr: var(--stroke-clr);

                --hat-graph-spacing: ${10}px;
                --hat-graph-node-size: ${30}px;
                --hat-graph-branch-height: ${20}px;
            }
            .graph-container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .actions {
                display: flex;
                flex-direction: column;
            }
            .parent {
                margin-left: 8px;
                margin-top: 16px;
            }
            .error {
                padding: 16px;
                max-width: 300px;
            }
            `}}]}}),r);t([o("react-trace-path-details")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"trace",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"selected",value:void 0},{kind:"field",decorators:[a()],key:"renderedNodes",value:()=>({})},{kind:"field",decorators:[a()],key:"trackedNodes",value:void 0},{kind:"field",decorators:[s()],key:"_view",value:()=>"config"},{kind:"method",key:"render",value:function(){return i`
            <div class="padded-box trace-info">
                ${this._renderSelectedTraceInfo()}
            </div>

            <div class="tabs top">
                ${[["config","Step Config"],["changed_variables","Changed Variables"]].map((([e,t])=>i`
                    <button
                        .view=${e}
                        class=${n({active:this._view===e})}
                        @click=${this._showTab}
                    >
                        ${t}
                    </button>
                `))}
            </div>
            ${"config"===this._view?this._renderSelectedConfig():this._renderChangedVars()}
        `}},{kind:"method",key:"_renderSelectedTraceInfo",value:function(){var e;const t=this.trace.trace;if(null===(e=this.selected)||void 0===e||!e.path)return"Select a node on the left for more information.";if(!(this.selected.path in t))return"This node was not executed and so no further trace information is available.";const r=[];let a=!1;for(const e of Object.keys(this.trace.trace)){if(a){if(e in this.renderedNodes)break}else{if(e!==this.selected.path)continue;a=!0}const o=t[e];r.push(o.map(((t,r)=>{const{path:a,timestamp:s,result:d,error:n,changed_variables:c,...h}=t;return!1===(null==d?void 0:d.enabled)?i`This node was disabled and skipped during execution so
                    no further trace information is available.`:i`
                    ${e===this.selected.path?"":i`<h2>${e.substr(this.selected.path.length+1)}</h2>`}
                    ${1===o.length?"":i`<h3>Iteration ${r+1}</h3>`}
                    Executed:
                    ${O(new Date(s),this.hass.locale)}
                    <br />
                    ${d?i`Result:
                            <pre>${B(d)}</pre>`:n?i`<div class="error">Error: ${n}</div>`:""}
                    ${0===Object.keys(h).length?"":i`<pre>${B(h)}</pre>`}
                `})))}return r}},{kind:"method",key:"_renderSelectedConfig",value:function(){var e;if(null===(e=this.selected)||void 0===e||!e.path)return"";const t=((e,t)=>{const r=t.split("/").reverse();let a=e;for(;r.length;){const e=r.pop(),t=Number(e);if(isNaN(t))a=a[e];else if(Array.isArray(a))a=a[t];else if(0!==t)throw new Error("If config is not an array, can only return index 0")}return a})(this.trace.config,this.selected.path);return t?i`
                <ha-code-editor
                    .value=${B(t).trimRight()}
                    readOnly
                    dir="ltr"
                ></ha-code-editor>`:"Unable to find config"}},{kind:"method",key:"_renderChangedVars",value:function(){const e=this.trace.trace[this.selected.path];return i`
        <div class="padded-box">
            ${e?e.map(((e,t)=>i`
                        ${t>0?i`<p>Iteration ${t+1}</p>`:""}
                        ${0===Object.keys(e.changed_variables||{}).length?"No variables changed":i`<pre>${B(e.changed_variables).trimRight()}</pre>`}
                    `)):""}
        </div>
        `}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"get",static:!0,key:"styles",value:function(){return[P,e`
                .padded-box {
                    margin: 16px;
                }

                :host(:not([narrow])) .trace-info {
                    min-height: 250px;
                }

                pre {
                    margin: 0;
                }

                .error {
                    color: var(--error-color);
                }
            `]}}]}}),r);let z=t([o("react-workflow-trace")],(function(t,r){class o extends r{constructor(...e){super(...e),t(this)}}return{F:o,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"workflowId",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"workflows",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[s()],key:"_entityId",value:void 0},{kind:"field",decorators:[s()],key:"_traces",value:void 0},{kind:"field",decorators:[s()],key:"_runId",value:void 0},{kind:"field",decorators:[s()],key:"_selected",value:void 0},{kind:"field",decorators:[s()],key:"_trace",value:void 0},{kind:"field",decorators:[s()],key:"_view",value:()=>"details"},{kind:"field",decorators:[$("react-script-graph")],key:"_graph",value:void 0},{kind:"method",key:"render",value:function(){var e;const t=this._entityId?this.hass.states[this._entityId]:void 0,r=this._graph,a=null==r?void 0:r.trackedNodes,o=null==r?void 0:r.renderedNodes,s=(null==t?void 0:t.attributes.friendly_name)||this._entityId;let d="";const c=i`
            <ha-icon-button
                .label=${this.hass.localize("ui.panel.config.automation.trace.refresh")}
                .path=${y}
                @click=${this._refreshTraces}
            ></ha-icon-button>
            <ha-icon-button
                .label=${this.hass.localize("ui.panel.config.automation.trace.download_trace")}
                .path=${m}
                .disabled=${!this._trace}
                @click=${this._downloadTrace}
            ></ha-icon-button>
        `;return i`
            ${d}
            <hass-tabs-subpage
                .hass=${this.hass}
                .narrow=${this.narrow}
                .route=${this.route}
                .tabs=${x.react}
            >
            ${this.narrow?i`<span slot="header">${s}</span>
                    <div slot="toolbar-icon">${c}</div>`:""}
            <div class="toolbar">
                ${this.narrow?"":i`<div>
                    ${s}
                    </div>`}
                ${this._traces&&this._traces.length>0?i`
                    <div>
                        <ha-icon-button
                            .label=${this.hass.localize("ui.panel.config.automation.trace.older_trace")}
                            .path=${w}
                            .disabled=${this._traces[this._traces.length-1].run_id===this._runId}
                            @click=${this._pickOlderTrace}
                        ></ha-icon-button>
                        <select .value=${this._runId} @change=${this._pickTrace}>
                        ${j(this._traces,(e=>e.run_id),(e=>i`<option value=${e.run_id}>
                                ${O(new Date(e.timestamp.start),this.hass.locale)}
                            </option>`))}
                        </select>
                        <ha-icon-button
                            .label=${this.hass.localize("ui.panel.config.automation.trace.newer_trace")}
                            .path=${N}
                            .disabled=${this._traces[0].run_id===this._runId}
                            @click=${this._pickNewerTrace}
                        ></ha-icon-button>
                    </div>
                    `:""}
                ${this.narrow?"":i`<div>${c}</div>`}
            </div>
    
            ${void 0===this._traces?i`<div class="container">Loading…</div>`:0===this._traces.length?i`<div class="container">No traces found</div>`:void 0===this._trace?"":i`
                    <div class="main">
                    <div class="graph">
                        <react-script-graph
                            .trace=${this._trace}
                            .selected=${null===(e=this._selected)||void 0===e?void 0:e.path}
                            @graph-node-selected=${this._pickNode}
                        ></react-script-graph>
                    </div>
    
                    <div class="info">
                        <div class="tabs top">
                            ${[["details","Step Details"],["config","Automation Config"]].map((([e,t])=>i`
                                <button
                                    tabindex="0"
                                    .view=${e}
                                    class=${n({active:this._view===e})}
                                    @click=${this._showTab}
                                >
                                    ${t}
                                </button>
                                `))}
                        </div>
                        ${void 0===this._selected||void 0===a?"":"details"===this._view?i`
                            <react-trace-path-details
                                .hass=${this.hass}
                                .narrow=${this.narrow}
                                .trace=${this._trace}
                                .selected=${this._selected}
                                .trackedNodes=${a}
                                .renderedNodes=${o}
                            ></react-trace-path-details>
                            `:i`
                            <ha-trace-config
                                .hass=${this.hass}
                                .trace=${this._trace}
                            ></ha-trace-config>
                            `}
                    </div>
                    </div>
                `}
            </hass-tabs-subpage>
        `}},{kind:"method",key:"firstUpdated",value:function(e){if(b(_(o.prototype),"firstUpdated",this).call(this,e),!this.workflowId)return;const t=new URLSearchParams(location.search);this._loadTraces(t.get("run_id")||void 0)}},{kind:"method",key:"updated",value:function(e){if(b(_(o.prototype),"updated",this).call(this,e),e.get("workflowId")&&(this._traces=void 0,this._entityId=void 0,this._runId=void 0,this._trace=void 0,this.workflowId&&this._loadTraces()),e.has("_runId")&&this._runId&&(this._trace=void 0,this._loadTrace()),e.has("workflows")&&this.workflowId&&!this._entityId){const e=this.workflows.find((e=>e.attributes.id===this.workflowId));this._entityId=null==e?void 0:e.entity_id}}},{kind:"method",key:"_pickOlderTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e+1].run_id,this._selected=void 0}},{kind:"method",key:"_pickNewerTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e-1].run_id,this._selected=void 0}},{kind:"method",key:"_pickTrace",value:function(e){this._runId=e.target.value,this._selected=void 0}},{kind:"method",key:"_pickNode",value:function(e){this._selected=e.detail}},{kind:"method",key:"_refreshTraces",value:function(){this._loadTraces()}},{kind:"method",key:"_loadTraces",value:async function(e){if(this._traces=await I(this.hass,this.workflowId),this._traces.reverse(),e&&(this._runId=e),this._runId&&!this._traces.some((e=>e.run_id===this._runId))){if(this._runId=void 0,this._selected=void 0,e){const e=new URLSearchParams(location.search);e.delete("run_id"),history.replaceState(null,"",`${location.pathname}?${e.toString()}`)}await E(this,{text:"Chosen trace is no longer available"})}!this._runId&&this._traces.length>0&&(this._runId=this._traces[0].run_id)}},{kind:"method",key:"_loadTrace",value:async function(){const e=await T(this.hass,this.workflowId,this._runId);this._trace=e}},{kind:"method",key:"_downloadTrace",value:function(){const e=document.createElement("a");e.download=`trace ${this._entityId} ${this._trace.timestamp.start}.json`,e.href=`data:application/json;charset=utf-8,${encodeURI(JSON.stringify({trace:this._trace},void 0,2))}`,e.click()}},{kind:"method",key:"_importTrace",value:function(){const e=prompt("Enter downloaded trace");e&&(localStorage.devTrace=e,this._loadLocalTrace(e))}},{kind:"method",key:"_loadLocalStorageTrace",value:function(){localStorage.devTrace&&this._loadLocalTrace(localStorage.devTrace)}},{kind:"method",key:"_loadLocalTrace",value:function(e){const t=JSON.parse(e);this._trace=t.trace}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"get",static:!0,key:"styles",value:function(){return[S,P,e`
                .toolbar {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  font-size: 20px;
                  height: var(--header-height);
                  padding: 0 16px;
                  background-color: var(--primary-background-color);
                  font-weight: 400;
                  color: var(--app-header-text-color, white);
                  border-bottom: var(--app-header-border-bottom, none);
                  box-sizing: border-box;
                }
        
                .toolbar > * {
                  display: flex;
                  align-items: center;
                }
        
                :host([narrow]) .toolbar > * {
                  display: contents;
                }
        
                .main {
                  height: calc(100% - 56px);
                  display: flex;
                  background-color: var(--card-background-color);
                }
        
                :host([narrow]) .main {
                  height: auto;
                  flex-direction: column;
                }
        
                .container {
                  padding: 16px;
                }
        
                .graph {
                  border-right: 1px solid var(--divider-color);
                  overflow-x: auto;
                  max-width: 50%;
                  padding-bottom: 16px;
                }
                :host([narrow]) .graph {
                  max-width: 100%;
                  justify-content: center;
                  display: flex;
                }
        
                .info {
                  flex: 1;
                  background-color: var(--card-background-color);
                }
        
                .linkButton {
                  color: var(--primary-text-color);
                }
              `]}}]}}),r);export{z as ReactWorkflowTrace};
