import{_ as e,s as t,$ as i,ar as a,n as d,e as l,f as s}from"./main-ac83c92b.js";import{s as o}from"./c.027db416.js";import"./c.3e14cfd3.js";e([d("ha-input-helper-text")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return i`<slot></slot>`}},{kind:"field",static:!0,key:"styles",value:()=>a`
    :host {
      display: block;
      color: var(--mdc-text-field-label-ink-color, rgba(0, 0, 0, 0.6));
      font-size: 0.75rem;
      padding-left: 16px;
      padding-right: 16px;
    }
  `}]}}),t),e([d("ha-base-time-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[l()],key:"label",value:void 0},{kind:"field",decorators:[l()],key:"helper",value:void 0},{kind:"field",decorators:[l({type:Boolean})],key:"autoValidate",value:()=>!1},{kind:"field",decorators:[l({type:Boolean})],key:"required",value:void 0},{kind:"field",decorators:[l({type:Number})],key:"format",value:()=>12},{kind:"field",decorators:[l({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[l({type:Number})],key:"days",value:()=>0},{kind:"field",decorators:[l({type:Number})],key:"hours",value:()=>0},{kind:"field",decorators:[l({type:Number})],key:"minutes",value:()=>0},{kind:"field",decorators:[l({type:Number})],key:"seconds",value:()=>0},{kind:"field",decorators:[l({type:Number})],key:"milliseconds",value:()=>0},{kind:"field",decorators:[l()],key:"dayLabel",value:()=>""},{kind:"field",decorators:[l()],key:"hourLabel",value:()=>""},{kind:"field",decorators:[l()],key:"minLabel",value:()=>""},{kind:"field",decorators:[l()],key:"secLabel",value:()=>""},{kind:"field",decorators:[l()],key:"millisecLabel",value:()=>""},{kind:"field",decorators:[l({type:Boolean})],key:"enableSecond",value:()=>!1},{kind:"field",decorators:[l({type:Boolean})],key:"enableMillisecond",value:()=>!1},{kind:"field",decorators:[l({type:Boolean})],key:"enableDay",value:()=>!1},{kind:"field",decorators:[l({type:Boolean})],key:"noHoursLimit",value:()=>!1},{kind:"field",decorators:[l()],key:"amPm",value:()=>"AM"},{kind:"field",decorators:[l()],key:"value",value:void 0},{kind:"method",key:"render",value:function(){return i`
      ${this.label?i`<label>${this.label}${this.required?"*":""}</label>`:""}
      <div class="time-input-wrap">
        ${this.enableDay?i`
              <ha-textfield
                id="day"
                type="number"
                inputmode="numeric"
                .value=${this.days}
                .label=${this.dayLabel}
                name="days"
                @input=${this._valueChanged}
                @focus=${this._onFocus}
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                min="0"
                .disabled=${this.disabled}
                suffix=":"
                class="hasSuffix"
              >
              </ha-textfield>
            `:""}

        <ha-textfield
          id="hour"
          type="number"
          inputmode="numeric"
          .value=${this.hours}
          .label=${this.hourLabel}
          name="hours"
          @input=${this._valueChanged}
          @focus=${this._onFocus}
          no-spinner
          .required=${this.required}
          .autoValidate=${this.autoValidate}
          maxlength="2"
          .max=${this._hourMax}
          min="0"
          .disabled=${this.disabled}
          suffix=":"
          class="hasSuffix"
        >
        </ha-textfield>
        <ha-textfield
          id="min"
          type="number"
          inputmode="numeric"
          .value=${this._formatValue(this.minutes)}
          .label=${this.minLabel}
          @input=${this._valueChanged}
          @focus=${this._onFocus}
          name="minutes"
          no-spinner
          .required=${this.required}
          .autoValidate=${this.autoValidate}
          maxlength="2"
          max="59"
          min="0"
          .disabled=${this.disabled}
          .suffix=${this.enableSecond?":":""}
          class=${this.enableSecond?"has-suffix":""}
        >
        </ha-textfield>
        ${this.enableSecond?i`<ha-textfield
              id="sec"
              type="number"
              inputmode="numeric"
              .value=${this._formatValue(this.seconds)}
              .label=${this.secLabel}
              @input=${this._valueChanged}
              @focus=${this._onFocus}
              name="seconds"
              no-spinner
              .required=${this.required}
              .autoValidate=${this.autoValidate}
              maxlength="2"
              max="59"
              min="0"
              .disabled=${this.disabled}
              .suffix=${this.enableMillisecond?":":""}
              class=${this.enableMillisecond?"has-suffix":""}
            >
            </ha-textfield>`:""}
        ${this.enableMillisecond?i`<ha-textfield
              id="millisec"
              type="number"
              .value=${this._formatValue(this.milliseconds,3)}
              .label=${this.millisecLabel}
              @input=${this._valueChanged}
              @focus=${this._onFocus}
              name="milliseconds"
              no-spinner
              .required=${this.required}
              .autoValidate=${this.autoValidate}
              maxlength="3"
              max="999"
              min="0"
              .disabled=${this.disabled}
            >
            </ha-textfield>`:""}
        ${24===this.format?"":i`<ha-select
              .required=${this.required}
              .value=${this.amPm}
              .disabled=${this.disabled}
              name="amPm"
              naturalMenuWidth
              fixedMenuPosition
              @selected=${this._valueChanged}
              @closed=${o}
            >
              <mwc-list-item value="AM">AM</mwc-list-item>
              <mwc-list-item value="PM">PM</mwc-list-item>
            </ha-select>`}
      </div>
      ${this.helper?i`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"method",key:"_valueChanged",value:function(e){this[e.target.name]="amPm"===e.target.name?e.target.value:Number(e.target.value);const t={hours:this.hours,minutes:this.minutes,seconds:this.seconds,milliseconds:this.milliseconds};12===this.format&&(t.amPm=this.amPm),s(this,"value-changed",{value:t})}},{kind:"method",key:"_onFocus",value:function(e){e.target.select()}},{kind:"method",key:"_formatValue",value:function(e,t=2){return e.toString().padStart(t,"0")}},{kind:"get",key:"_hourMax",value:function(){return this.noHoursLimit?null:12===this.format?12:23}},{kind:"field",static:!0,key:"styles",value:()=>a`
    :host {
      display: block;
    }
    .time-input-wrap {
      display: flex;
      border-radius: var(--mdc-shape-small, 4px) var(--mdc-shape-small, 4px) 0 0;
      overflow: hidden;
      position: relative;
    }
    ha-textfield {
      width: 40px;
      text-align: center;
      --mdc-shape-small: 0;
      --text-field-appearance: none;
      --text-field-padding: 0 4px;
      --text-field-suffix-padding-left: 2px;
      --text-field-suffix-padding-right: 0;
      --text-field-text-align: center;
    }
    ha-textfield.hasSuffix {
      --text-field-padding: 0 0 0 4px;
    }
    ha-textfield:first-child {
      --text-field-border-top-left-radius: var(--mdc-shape-medium);
    }
    ha-textfield:last-child {
      --text-field-border-top-right-radius: var(--mdc-shape-medium);
    }
    ha-select {
      --mdc-shape-small: 0;
      width: 85px;
    }
    label {
      -moz-osx-font-smoothing: grayscale;
      -webkit-font-smoothing: antialiased;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      line-height: var(--mdc-typography-body2-line-height, 1.25rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      letter-spacing: var(
        --mdc-typography-body2-letter-spacing,
        0.0178571429em
      );
      text-decoration: var(--mdc-typography-body2-text-decoration, inherit);
      text-transform: var(--mdc-typography-body2-text-transform, inherit);
      color: var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));
      padding-left: 4px;
    }
  `}]}}),t);
