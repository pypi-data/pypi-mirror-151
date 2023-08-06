import{J as t,K as e,I as i,F as s,a as o,f as n,e as a,t as l,$ as r,eg as d,j as h,r as c,n as m,h as u,W as p,H as f}from"./main-e088bb19.js";import{r as v}from"./c.44ff3154.js";import"./c.0bdb0337.js";import{c as g}from"./c.74178c3e.js";import{c as _}from"./c.166c4b5c.js";import{M as y}from"./c.36f258ab.js";import{i as b,u as $,r as k,b as w}from"./c.1e4d0185.js";import{a as A,s as C}from"./c.d8002660.js";import"./c.7943fa91.js";import"./c.efa39a97.js";import"./c.8e28b461.js";import"./c.4cc25ce4.js";import"./c.e9faf9fb.js";import"./c.c8c7ce92.js";import"./c.fcc8c8a6.js";import"./c.a6191dc5.js";import"./c.743a15a1.js";import"./c.d554af2f.js";import"./c.2ef5c8dd.js";import"./c.7312bad4.js";import"./c.3b8f3ca0.js";import"./c.ceb1e431.js";import"./c.259a5b7b.js";import"./c.06c5e585.js";import"./c.2b12d4b5.js";const x=(t,e)=>{var i,s;const o=t._$AN;if(void 0===o)return!1;for(const t of o)null===(s=(i=t)._$AO)||void 0===s||s.call(i,e,!1),x(t,e);return!0},j=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},I=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),O(e)}};function z(t){void 0!==this._$AN?(j(this),this._$AM=t,I(this)):this._$AM=t}function S(t,e=!1,i=0){const s=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(e)if(Array.isArray(s))for(let t=i;t<s.length;t++)x(s[t],!1),j(s[t]);else null!=s&&(x(s,!1),j(s));else x(this,t)}const O=t=>{var i,s,o,n;t.type==e.CHILD&&(null!==(i=(o=t)._$AP)&&void 0!==i||(o._$AP=S),null!==(s=(n=t)._$AQ)&&void 0!==s||(n._$AQ=z))};class D extends t{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),I(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,s;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(s=this.disconnected)||void 0===s||s.call(this)),e&&(x(this,t),j(this))}setValue(t){if(v(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}const N=new WeakMap;let F=0;const M=new Map,U=new WeakSet,E=()=>new Promise((t=>requestAnimationFrame(t))),P=(t,e)=>{const i=t-e;return 0===i?void 0:i},H=(t,e)=>{const i=t/e;return 1===i?void 0:i},K={left:(t,e)=>{const i=P(t,e);return{value:i,transform:i&&`translateX(${i}px)`}},top:(t,e)=>{const i=P(t,e);return{value:i,transform:i&&`translateY(${i}px)`}},width:(t,e)=>{const i=H(t,e);return{value:i,transform:i&&`scaleX(${i})`}},height:(t,e)=>{const i=H(t,e);return{value:i,transform:i&&`scaleY(${i})`}}},L={duration:333,easing:"ease-in-out"},W=["left","top","width","height","opacity","color","background"],R=new WeakMap;const T=i(class extends D{constructor(t){if(super(t),this.t=null,this.i=null,this.o=!0,this.shouldLog=!1,t.type===e.CHILD)throw Error("The `animate` directive must be used in attribute position.");this.createFinished()}createFinished(){var t;null===(t=this.resolveFinished)||void 0===t||t.call(this),this.finished=new Promise((t=>{this.h=t}))}async resolveFinished(){var t;null===(t=this.h)||void 0===t||t.call(this),this.h=void 0}render(t){return s}getController(){return N.get(this.l)}isDisabled(){var t;return this.options.disabled||(null===(t=this.getController())||void 0===t?void 0:t.disabled)}update(t,[e]){var i;const s=void 0===this.l;return s&&(this.l=null===(i=t.options)||void 0===i?void 0:i.host,this.l.addController(this),this.element=t.element,R.set(this.element,this)),this.optionsOrCallback=e,(s||"function"!=typeof e)&&this.u(e),this.render(e)}u(t){var e,i;t=null!=t?t:{};const s=this.getController();void 0!==s&&((t={...s.defaultOptions,...t}).keyframeOptions={...s.defaultOptions.keyframeOptions,...t.keyframeOptions}),null!==(e=(i=t).properties)&&void 0!==e||(i.properties=W),this.options=t}v(){const t={},e=this.element.getBoundingClientRect(),i=getComputedStyle(this.element);return this.options.properties.forEach((s=>{var o;const n=null!==(o=e[s])&&void 0!==o?o:K[s]?void 0:i[s],a=Number(n);t[s]=isNaN(a)?n+"":a})),t}p(){let t,e=!0;return this.options.guard&&(t=this.options.guard(),e=((t,e)=>{if(Array.isArray(t)){if(Array.isArray(e)&&e.length===t.length&&t.every(((t,i)=>t===e[i])))return!1}else if(e===t)return!1;return!0})(t,this.m)),this.o=this.l.hasUpdated&&!this.isDisabled()&&!this.isAnimating()&&e&&this.element.isConnected,this.o&&(this.m=Array.isArray(t)?Array.from(t):t),this.o}hostUpdate(){var t;"function"==typeof this.optionsOrCallback&&this.u(this.optionsOrCallback()),this.p()&&(this.g=this.v(),this.t=null!==(t=this.t)&&void 0!==t?t:this.element.parentNode,this.i=this.element.nextSibling)}async hostUpdated(){if(!this.o||!this.element.isConnected||this.options.skipInitial&&!this.isHostRendered)return;let t;this.prepare(),await E;const e=this.A(),i=this._(this.options.keyframeOptions,e),s=this.v();if(void 0!==this.g){const{from:i,to:o}=this.j(this.g,s,e);this.log("measured",[this.g,s,i,o]),t=this.calculateKeyframes(i,o)}else{const i=M.get(this.options.inId);if(i){M.delete(this.options.inId);const{from:o,to:n}=this.j(i,s,e);t=this.calculateKeyframes(o,n),t=this.options.in?[{...this.options.in[0],...t[0]},...this.options.in.slice(1),t[1]]:t,F++,t.forEach((t=>t.zIndex=F))}else this.options.in&&(t=[...this.options.in,{}])}this.animate(t,i)}resetStyles(){var t;void 0!==this.S&&(this.element.setAttribute("style",null!==(t=this.S)&&void 0!==t?t:""),this.S=void 0)}commitStyles(){var t,e;this.S=this.element.getAttribute("style"),null===(t=this.webAnimation)||void 0===t||t.commitStyles(),null===(e=this.webAnimation)||void 0===e||e.cancel()}reconnected(){}async disconnected(){var t;if(!this.o)return;if(void 0!==this.options.id&&M.set(this.options.id,this.g),void 0===this.options.out)return;if(this.prepare(),await E(),null===(t=this.t)||void 0===t?void 0:t.isConnected){const t=this.i&&this.i.parentNode===this.t?this.i:null;if(this.t.insertBefore(this.element,t),this.options.stabilizeOut){const t=this.v();this.log("stabilizing out");const e=this.g.left-t.left,i=this.g.top-t.top;!("static"===getComputedStyle(this.element).position)||0===e&&0===i||(this.element.style.position="relative"),0!==e&&(this.element.style.left=e+"px"),0!==i&&(this.element.style.top=i+"px")}}const e=this._(this.options.keyframeOptions);await this.animate(this.options.out,e),this.element.remove()}prepare(){this.createFinished()}start(){var t,e;null===(e=(t=this.options).onStart)||void 0===e||e.call(t,this)}didFinish(t){var e,i;t&&(null===(i=(e=this.options).onComplete)||void 0===i||i.call(e,this)),this.g=void 0,this.animatingProperties=void 0,this.frames=void 0,this.resolveFinished()}A(){const t=[];for(let e=this.element.parentNode;e;e=null==e?void 0:e.parentNode){const i=R.get(e);i&&!i.isDisabled()&&i&&t.push(i)}return t}get isHostRendered(){const t=U.has(this.l);return t||this.l.updateComplete.then((()=>{U.add(this.l)})),t}_(t,e=this.A()){const i={...L};return e.forEach((t=>Object.assign(i,t.options.keyframeOptions))),Object.assign(i,t),i}j(t,e,i){t={...t},e={...e};const s=i.map((t=>t.animatingProperties)).filter((t=>void 0!==t));let o=1,n=1;return void 0!==s&&(s.forEach((t=>{t.width&&(o/=t.width),t.height&&(n/=t.height)})),void 0!==t.left&&void 0!==e.left&&(t.left=o*t.left,e.left=o*e.left),void 0!==t.top&&void 0!==e.top&&(t.top=n*t.top,e.top=n*e.top)),{from:t,to:e}}calculateKeyframes(t,e,i=!1){var s;const o={},n={};let a=!1;const l={};for(const i in e){const r=t[i],d=e[i];if(i in K){const t=K[i];if(void 0===r||void 0===d)continue;const e=t(r,d);void 0!==e.transform&&(l[i]=e.value,a=!0,o.transform=`${null!==(s=o.transform)&&void 0!==s?s:""} ${e.transform}`)}else r!==d&&void 0!==r&&void 0!==d&&(a=!0,o[i]=r,n[i]=d)}return o.transformOrigin=n.transformOrigin=i?"center center":"top left",this.animatingProperties=l,a?[o,n]:void 0}async animate(t,e=this.options.keyframeOptions){this.start(),this.frames=t;let i=!1;if(!this.isAnimating()&&!this.isDisabled()&&(this.options.onFrames&&(this.frames=t=this.options.onFrames(this),this.log("modified frames",t)),void 0!==t)){this.log("animate",[t,e]),i=!0,this.webAnimation=this.element.animate(t,e);const s=this.getController();null==s||s.add(this);try{await this.webAnimation.finished}catch(t){}null==s||s.remove(this)}return this.didFinish(i),i}isAnimating(){var t,e;return"running"===(null===(t=this.webAnimation)||void 0===t?void 0:t.playState)||(null===(e=this.webAnimation)||void 0===e?void 0:e.pending)}log(t,e){this.shouldLog&&!this.isDisabled()&&console.log(t,this.options.id,e)}});o([m("ha-media-upload-button")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"currentItem",value:void 0},{kind:"field",decorators:[l()],key:"_uploading",value:()=>0},{kind:"method",key:"render",value:function(){return this.currentItem&&b(this.currentItem.media_content_id||"")?r`
      <mwc-button
        .label=${this._uploading>0?this.hass.localize("ui.components.media-browser.file_management.uploading",{count:this._uploading}):this.hass.localize("ui.components.media-browser.file_management.add_media")}
        .disabled=${this._uploading>0}
        @click=${this._startUpload}
      >
        ${this._uploading>0?r`
              <ha-circular-progress
                size="tiny"
                active
                alt=""
                slot="icon"
              ></ha-circular-progress>
            `:r` <ha-svg-icon .path=${d} slot="icon"></ha-svg-icon> `}
      </mwc-button>
    `:r``}},{kind:"method",key:"_startUpload",value:async function(){if(this._uploading>0)return;const t=document.createElement("input");t.type="file",t.accept="audio/*,video/*,image/*",t.multiple=!0,t.addEventListener("change",(async()=>{h(this,"uploading");const e=t.files;document.body.removeChild(t);const i=this.currentItem.media_content_id;for(let t=0;t<e.length;t++){this._uploading=e.length-t;try{await $(this.hass,i,e[t])}catch(t){A(this,{text:this.hass.localize("ui.components.media-browser.file_management.upload_failed",{reason:t.message||t})});break}}this._uploading=0,h(this,"media-refresh")}),{once:!0}),t.style.display="none",document.body.append(t),t.click()}},{kind:"field",static:!0,key:"styles",value:()=>c`
    mwc-button {
      /* We use icon + text to show disabled state */
      --mdc-button-disabled-ink-color: --mdc-theme-primary;
    }

    ha-svg-icon[slot="icon"],
    ha-circular-progress[slot="icon"] {
      vertical-align: middle;
    }
  `}]}}),n),o([m("dialog-media-manage")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[l()],key:"_currentItem",value:void 0},{kind:"field",decorators:[l()],key:"_params",value:void 0},{kind:"field",decorators:[l()],key:"_uploading",value:()=>!1},{kind:"field",decorators:[l()],key:"_deleting",value:()=>!1},{kind:"field",decorators:[l()],key:"_selected",value:()=>new Set},{kind:"field",key:"_filesChanged",value:()=>!1},{kind:"method",key:"showDialog",value:function(t){this._params=t,this._refreshMedia()}},{kind:"method",key:"closeDialog",value:function(){this._filesChanged&&this._params.onClose&&this._params.onClose(),this._params=void 0,this._currentItem=void 0,this._uploading=!1,this._deleting=!1,this._filesChanged=!1,h(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){var t,e,i,s;if(!this._params)return r``;const o=(null===(t=this._currentItem)||void 0===t||null===(e=t.children)||void 0===e?void 0:e.filter((t=>!t.can_expand)))||[];let n=0;return r`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        hideActions
        flexContent
        .heading=${this._params.currentItem.title}
        @closed=${this.closeDialog}
      >
        <ha-header-bar slot="heading">
          ${0===this._selected.size?r`
                <span slot="title">
                  ${this.hass.localize("ui.components.media-browser.file_management.title")}
                </span>

                <ha-media-upload-button
                  .disabled=${this._deleting}
                  .hass=${this.hass}
                  .currentItem=${this._params.currentItem}
                  @uploading=${this._startUploading}
                  @media-refresh=${this._doneUploading}
                  slot="actionItems"
                ></ha-media-upload-button>
                ${this._uploading?"":r`
                      <ha-icon-button
                        .label=${this.hass.localize("ui.dialogs.generic.close")}
                        .path=${u}
                        dialogAction="close"
                        slot="actionItems"
                        class="header_button"
                        dir=${_(this.hass)}
                      ></ha-icon-button>
                    `}
              `:r`
                <mwc-button
                  class="danger"
                  slot="title"
                  .disabled=${this._deleting}
                  .label=${this.hass.localize("ui.components.media-browser.file_management."+(this._deleting?"deleting":"delete"),{count:this._selected.size})}
                  @click=${this._handleDelete}
                >
                  <ha-svg-icon .path=${p} slot="icon"></ha-svg-icon>
                </mwc-button>

                ${this._deleting?"":r`
                      <mwc-button
                        slot="actionItems"
                        .label=${"Deselect all"}
                        @click=${this._handleDeselectAll}
                      >
                        <ha-svg-icon
                          .path=${u}
                          slot="icon"
                        ></ha-svg-icon>
                      </mwc-button>
                    `}
              `}
        </ha-header-bar>
        ${this._currentItem?o.length?r`
              <mwc-list multi @selected=${this._handleSelected}>
                ${g(o,(t=>t.media_content_id),(t=>{const e=r`
                      <ha-svg-icon
                        slot="graphic"
                        .path=${y["directory"===t.media_class&&t.children_media_class||t.media_class].icon}
                      ></ha-svg-icon>
                    `;return r`
                      <ha-check-list-item
                        ${T({id:t.media_content_id,skipInitial:!0})}
                        graphic="icon"
                        .disabled=${this._uploading||this._deleting}
                        .selected=${this._selected.has(n++)}
                        .item=${t}
                      >
                        ${e} ${t.title}
                      </ha-check-list-item>
                    `}))}
              </mwc-list>
            `:r`<div class="no-items">
              <p>
                ${this.hass.localize("ui.components.media-browser.file_management.no_items")}
              </p>
              ${null!==(i=this._currentItem)&&void 0!==i&&null!==(s=i.children)&&void 0!==s&&s.length?r`<span class="folders"
                    >${this.hass.localize("ui.components.media-browser.file_management.folders_not_supported")}</span
                  >`:""}
            </div>`:r`
              <div class="refresh">
                <ha-circular-progress active></ha-circular-progress>
              </div>
            `}
      </ha-dialog>
    `}},{kind:"method",key:"_handleSelected",value:function(t){this._selected=t.detail.index}},{kind:"method",key:"_startUploading",value:function(){this._uploading=!0,this._filesChanged=!0}},{kind:"method",key:"_doneUploading",value:function(){this._uploading=!1,this._refreshMedia()}},{kind:"method",key:"_handleDeselectAll",value:function(){this._selected.size&&(this._selected=new Set)}},{kind:"method",key:"_handleDelete",value:async function(){if(!await C(this,{text:this.hass.localize("ui.components.media-browser.file_management.confirm_delete",{count:this._selected.size}),warning:!0}))return;this._filesChanged=!0,this._deleting=!0;const t=[];let e=0;this._currentItem.children.forEach((i=>{i.can_expand||this._selected.has(e++)&&t.push(i)}));try{await Promise.all(t.map((async t=>{await k(this.hass,t.media_content_id),this._currentItem={...this._currentItem,children:this._currentItem.children.filter((e=>e!==t))}})))}finally{this._deleting=!1,this._selected=new Set}}},{kind:"method",key:"_refreshMedia",value:async function(){this._selected=new Set,this._currentItem=void 0,this._currentItem=await w(this.hass,this._params.currentItem.media_content_id)}},{kind:"get",static:!0,key:"styles",value:function(){return[f,c`
        ha-dialog {
          --dialog-z-index: 8;
          --dialog-content-padding: 0;
        }

        @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --dialog-surface-position: fixed;
            --dialog-surface-top: 40px;
            --mdc-dialog-max-height: calc(100vh - 72px);
          }
        }

        ha-header-bar {
          --mdc-theme-on-primary: var(--primary-text-color);
          --mdc-theme-primary: var(--mdc-theme-surface);
          flex-shrink: 0;
          border-bottom: 1px solid var(--divider-color, rgba(0, 0, 0, 0.12));
        }

        ha-media-upload-button,
        mwc-button {
          --mdc-theme-primary: var(--mdc-theme-on-primary);
        }

        .danger {
          --mdc-theme-primary: var(--error-color);
        }

        ha-svg-icon[slot="icon"] {
          vertical-align: middle;
        }

        .refresh {
          display: flex;
          height: 200px;
          justify-content: center;
          align-items: center;
        }

        .no-items {
          text-align: center;
          padding: 16px;
        }
        .folders {
          color: var(--secondary-text-color);
          font-style: italic;
        }
      `]}}]}}),n);
