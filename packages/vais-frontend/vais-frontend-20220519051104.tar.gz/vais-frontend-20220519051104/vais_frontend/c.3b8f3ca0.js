import{a as e,f as t,e as i,$ as n,r as o,n as r}from"./main-e088bb19.js";import"./c.ceb1e431.js";e([r("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[i({type:Boolean,attribute:"three-line"})],key:"threeLine",value:()=>!1},{kind:"method",key:"render",value:function(){return n`
      <div class="prefix-wrap">
        <slot name="prefix"></slot>
        <paper-item-body
          ?two-line=${!this.threeLine}
          ?three-line=${this.threeLine}
        >
          <slot name="heading"></slot>
          <div secondary><slot name="description"></slot></div>
        </paper-item-body>
      </div>
      <div class="content"><slot></slot></div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host {
        display: flex;
        padding: 0 16px;
        align-content: normal;
        align-self: auto;
        align-items: center;
      }
      paper-item-body {
        padding: 8px 16px 8px 0;
      }
      paper-item-body[two-line] {
        min-height: calc(
          var(--paper-item-body-two-line-min-height, 72px) - 16px
        );
        flex: 1;
      }
      .content {
        display: contents;
      }
      :host(:not([narrow])) .content {
        display: flex;
        justify-content: flex-end;
        flex: 1;
        padding: 16px 0;
      }
      .content ::slotted(*) {
        width: var(--settings-row-content-width);
      }
      :host([narrow]) {
        align-items: normal;
        flex-direction: column;
        border-top: 1px solid var(--divider-color);
        padding-bottom: 8px;
      }
      ::slotted(ha-switch) {
        padding: 16px 0;
      }
      div[secondary] {
        white-space: normal;
      }
      .prefix-wrap {
        display: contents;
      }
      :host([narrow]) .prefix-wrap {
        display: flex;
        align-items: center;
      }
    `}}]}}),t);
