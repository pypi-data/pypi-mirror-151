import{cx as e,cq as i}from"./main-ac83c92b.js";import"./c.3e14cfd3.js";customElements.define("ha-labeled-slider",class extends e{static get template(){return i`
      <style>
        :host {
          display: block;
        }

        .title {
          margin: 5px 0 8px;
          color: var(--primary-text-color);
        }

        .slider-container {
          display: flex;
        }

        ha-icon {
          margin-top: 4px;
          color: var(--secondary-text-color);
        }

        ha-slider {
          flex-grow: 1;
          background-image: var(--ha-slider-background);
          border-radius: 4px;
        }
      </style>

      <div class="title">[[_getTitle()]]</div>
      <div class="extra-container"><slot name="extra"></slot></div>
      <div class="slider-container">
        <ha-icon icon="[[icon]]" hidden$="[[!icon]]"></ha-icon>
        <ha-slider
          min="[[min]]"
          max="[[max]]"
          step="[[step]]"
          pin="[[pin]]"
          disabled="[[disabled]]"
          value="{{value}}"
        ></ha-slider>
      </div>
      <template is="dom-if" if="[[helper]]">
        <ha-input-helper-text>[[helper]]</ha-input-helper-text>
      </template>
    `}_getTitle(){return`${this.caption}${this.required?"*":""}`}static get properties(){return{caption:String,disabled:Boolean,required:Boolean,min:Number,max:Number,pin:Boolean,step:Number,helper:String,extra:{type:Boolean,value:!1},ignoreBarTouch:{type:Boolean,value:!0},icon:{type:String,value:""},value:{type:Number,notify:!0}}}});
