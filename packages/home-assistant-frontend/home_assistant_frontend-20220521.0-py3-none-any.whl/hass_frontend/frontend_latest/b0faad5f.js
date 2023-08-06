"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[38634],{43793:(e,t,i)=>{i.d(t,{x:()=>r});const r=(e,t)=>e.substring(0,t.length)===t},55422:(e,t,i)=>{i.a(e,(async e=>{i.d(t,{jV:()=>l,sS:()=>u,rM:()=>h,tf:()=>y});var r=i(49706),n=i(58831),o=i(29171),s=i(56007),a=e([o]);o=(a.then?await a:a)[0];const c="ui.components.logbook.messages",l=["proximity","sensor"],d={},u=async(e,t,i)=>{const r=await e.loadBackendTranslation("device_class");return p(e,r,await m(e,t,void 0,void 0,i))},h=async(e,t,i,r,n)=>{const o=await e.loadBackendTranslation("device_class");return p(e,o,null!=n&&n.length?await m(e,t,i,r,void 0,n):await f(e,t,i,r))},p=(e,t,i)=>{for(const r of i){const i=e.states[r.entity_id];r.state&&i&&(r.message=v(e,t,r.state,i,(0,n.M)(r.entity_id)))}return i},f=async(e,t,i,r)=>{const n=r?r.toString():"*",o=`${t}${i}`;if(d[o]||(d[o]={}),n in d[o])return d[o][n];if(r&&d[o]["*"]){return(await d[o]["*"]).filter((e=>e.entity_id&&r.includes(e.entity_id)))}return d[o][n]=m(e,t,i,r),d[o][n]},m=(e,t,i,r,n,o)=>{if((r||o)&&(!r||0===r.length)&&(!o||0===o.length))return Promise.resolve([]);const s={type:"logbook/get_events",start_time:t};return i&&(s.end_time=i),null!=r&&r.length&&(s.entity_ids=r),null!=o&&o.length&&(s.device_ids=o),n&&(s.context_id=n),e.callWS(s)},y=(e,t)=>{d[`${e}${t}`]={}},v=(e,t,i,n,a)=>{switch(a){case"device_tracker":case"person":return"not_home"===i?t(`${c}.was_away`):"home"===i?t(`${c}.was_at_home`):t(`${c}.was_at_state`,"state",i);case"sun":return t("above_horizon"===i?`${c}.rose`:`${c}.set`);case"binary_sensor":{const e=i===r.uo,o=i===r.lC,s=n.attributes.device_class;switch(s){case"battery":if(e)return t(`${c}.was_low`);if(o)return t(`${c}.was_normal`);break;case"connectivity":if(e)return t(`${c}.was_connected`);if(o)return t(`${c}.was_disconnected`);break;case"door":case"garage_door":case"opening":case"window":if(e)return t(`${c}.was_opened`);if(o)return t(`${c}.was_closed`);break;case"lock":if(e)return t(`${c}.was_unlocked`);if(o)return t(`${c}.was_locked`);break;case"plug":if(e)return t(`${c}.was_plugged_in`);if(o)return t(`${c}.was_unplugged`);break;case"presence":if(e)return t(`${c}.was_at_home`);if(o)return t(`${c}.was_away`);break;case"safety":if(e)return t(`${c}.was_unsafe`);if(o)return t(`${c}.was_safe`);break;case"cold":case"gas":case"heat":case"moisture":case"motion":case"occupancy":case"power":case"problem":case"smoke":case"sound":case"vibration":if(e)return t(`${c}.detected_device_class`,{device_class:t(`component.binary_sensor.device_class.${s}`)});if(o)return t(`${c}.cleared_device_class`,{device_class:t(`component.binary_sensor.device_class.${s}`)});break;case"tamper":if(e)return t(`${c}.detected_tampering`);if(o)return t(`${c}.cleared_tampering`)}break}case"cover":switch(i){case"open":return t(`${c}.was_opened`);case"opening":return t(`${c}.is_opening`);case"closing":return t(`${c}.is_closing`);case"closed":return t(`${c}.was_closed`)}break;case"lock":if("unlocked"===i)return t(`${c}.was_unlocked`);if("locked"===i)return t(`${c}.was_locked`)}return i===r.uo?t(`${c}.turned_on`):i===r.lC?t(`${c}.turned_off`):s.V_.includes(i)?t(`${c}.became_unavailable`):e.localize(`${c}.changed_to_state`,"state",n?(0,o.D)(t,n,e.locale,i):i)}}))},97389:(e,t,i)=>{if(i.d(t,{mA:()=>n,lj:()=>o,U_:()=>s,nV:()=>a,Zm:()=>c}),32143==i.j)var r=i(43793);const n=(e,t,i,r)=>e.callWS({type:"trace/get",domain:t,item_id:i,run_id:r}),o=(e,t,i)=>e.callWS({type:"trace/list",domain:t,item_id:i}),s=(e,t,i)=>e.callWS({type:"trace/contexts",domain:t,item_id:i}),a=(e,t)=>{const i=t.split("/").reverse();let r=e;for(;i.length;){const e=i.pop(),t=Number(e);if(isNaN(t)){const t=r[e];if(!t&&"sequence"===e)continue;r=t}else if(Array.isArray(r))r=r[t];else if(0!==t)throw new Error("If config is not an array, can only return index 0")}return r},c=e=>"trigger"===e||(0,r.x)(e,"trigger/")},44198:(e,t,i)=>{i.a(e,(async e=>{i(9874);var t=i(37500),r=i(33310),n=i(8636),o=i(49706),s=i(12198),a=i(49684),c=i(25516),l=i(47181),d=i(58831),u=i(7323),h=i(87744),p=(i(3143),i(31206),i(42952)),f=i(11654),m=i(11254),y=e([a,s,p]);function v(){v=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!b(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return x(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?x(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=$(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function _(e){var t,i=$(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function g(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function b(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function $(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function x(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}[a,s,p]=y.then?await y:y;const E={script_started:"from_script"};!function(e,t,i,r){var n=v();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(k(o.descriptor)||k(n.descriptor)){if(b(o)||b(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(b(o)){if(b(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}g(o,n)}else t.push(o)}return t}(s.d.map(_)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("ha-logbook-renderer")],(function(e,i){return{F:class extends i{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"userIdToName",value:()=>({})},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"traceContexts",value:()=>({})},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"entries",value:()=>[]},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"narrow"})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({attribute:"rtl",type:Boolean})],key:"_rtl",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"virtualize",reflect:!0})],key:"virtualize",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-icon"})],key:"noIcon",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-name"})],key:"noName",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"relative-time"})],key:"relativeTime",value:()=>!1},{kind:"field",decorators:[(0,c.i)(".container")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){const t=e.get("hass"),i=void 0===t||t.locale!==this.hass.locale;return e.has("entries")||e.has("traceContexts")||i}},{kind:"method",key:"updated",value:function(e){const t=e.get("hass");void 0!==t&&t.language===this.hass.language||(this._rtl=(0,h.HE)(this.hass))}},{kind:"method",key:"render",value:function(){var e;return null!==(e=this.entries)&&void 0!==e&&e.length?t.dy`
      <div
        class="container ha-scrollbar ${(0,n.$)({narrow:this.narrow,rtl:this._rtl,"no-name":this.noName,"no-icon":this.noIcon})}"
        @scroll=${this._saveScrollPos}
      >
        ${this.virtualize?t.dy`<lit-virtualizer
              scroller
              class="ha-scrollbar"
              .items=${this.entries}
              .renderItem=${this._renderLogbookItem}
            >
            </lit-virtualizer>`:this.entries.map(((e,t)=>this._renderLogbookItem(e,t)))}
      </div>
    `:t.dy`
        <div class="container no-entries" .dir=${(0,h.$3)(this._rtl)}>
          ${this.hass.localize("ui.components.logbook.entries_not_found")}
        </div>
      `}},{kind:"field",key:"_renderLogbookItem",value(){return(e,i)=>{var r;if(!e||void 0===i)return t.dy``;const c=[],l=this.entries[i-1],h=e.entity_id?this.hass.states[e.entity_id]:void 0,p=e.context_user_id&&this.userIdToName[e.context_user_id],f=e.entity_id?(0,d.M)(e.entity_id):e.domain,y=e.entity_id?{entity_id:e.entity_id,state:e.state,attributes:{device_class:null==h?void 0:h.attributes.device_class,source_type:null==h?void 0:h.attributes.source_type,has_date:null==h?void 0:h.attributes.has_date,has_time:null==h?void 0:h.attributes.has_time,entity_picture_local:o.iY.has(f)||null==h?void 0:h.attributes.entity_picture_local,entity_picture:o.iY.has(f)||null==h?void 0:h.attributes.entity_picture}}:void 0,v=!y&&!e.icon&&f&&(0,u.p)(this.hass,f)?(0,m.X)({domain:f,type:"icon",useFallback:!0,darkOptimized:null===(r=this.hass.themes)||void 0===r?void 0:r.darkMode}):void 0;return t.dy`
      <div class="entry-container">
        ${0===i||null!=e&&e.when&&null!=l&&l.when&&new Date(1e3*e.when).toDateString()!==new Date(1e3*l.when).toDateString()?t.dy`
              <h4 class="date">
                ${(0,s.p6)(new Date(1e3*e.when),this.hass.locale)}
              </h4>
            `:t.dy``}

        <div class="entry ${(0,n.$)({"no-entity":!e.entity_id})}">
          <div class="icon-message">
            ${this.noIcon?"":t.dy`
                  <state-badge
                    .hass=${this.hass}
                    .overrideIcon=${e.icon}
                    .overrideImage=${v}
                    .stateObj=${e.icon?void 0:y}
                    .stateColor=${!1}
                  ></state-badge>
                `}
            <div class="message-relative_time">
              <div class="message">
                ${this.noName?"":this._renderEntity(e.entity_id,e.name)}
                ${e.message?t.dy`${this._formatMessageWithPossibleEntity(e.message,c,e.entity_id)}`:e.source?t.dy` ${this._formatMessageWithPossibleEntity(e.source,c,void 0,"ui.components.logbook.by")}`:""}
                ${p?` ${this.hass.localize("ui.components.logbook.by_user")} ${p}`:""}
                ${e.context_event_type?this._formatEventBy(e,c):""}
                ${e.context_message?t.dy` ${this._formatMessageWithPossibleEntity(e.context_message,c,e.context_entity_id,"ui.components.logbook.for")}`:""}
                ${e.context_entity_id&&!c.includes(e.context_entity_id)?t.dy` ${this.hass.localize("ui.components.logbook.for")}
                    ${this._renderEntity(e.context_entity_id,e.context_entity_id_name)}`:""}
              </div>
              <div class="secondary">
                <span
                  >${(0,a.Vu)(new Date(1e3*e.when),this.hass.locale)}</span
                >
                -
                <ha-relative-time
                  .hass=${this.hass}
                  .datetime=${1e3*e.when}
                  capitalize
                ></ha-relative-time>
                ${["script","automation"].includes(e.domain)&&e.context_id in this.traceContexts?t.dy`
                      -
                      <a
                        href=${`/config/${this.traceContexts[e.context_id].domain}/trace/${"script"===this.traceContexts[e.context_id].domain?`script.${this.traceContexts[e.context_id].item_id}`:this.traceContexts[e.context_id].item_id}?run_id=${this.traceContexts[e.context_id].run_id}`}
                        @click=${this._close}
                        >${this.hass.localize("ui.components.logbook.show_trace")}</a
                      >
                    `:""}
              </div>
            </div>
          </div>
        </div>
      </div>
    `}}},{kind:"method",decorators:[(0,r.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_formatEventBy",value:function(e,i){return"call_service"===e.context_event_type?`${this.hass.localize("ui.components.logbook.from_service")} ${e.context_domain}.${e.context_service}`:"automation_triggered"===e.context_event_type?i.includes(e.context_entity_id)?"":(i.push(e.context_entity_id),t.dy`${this.hass.localize("ui.components.logbook.from_automation")}
      ${this._renderEntity(e.context_entity_id,e.context_name)}`):e.context_name?`${this.hass.localize("ui.components.logbook.from")} ${e.context_name}`:"state_changed"===e.context_event_type?"":e.context_event_type in E?`${this.hass.localize(`ui.components.logbook.${E[e.context_event_type]}`)}`:`${this.hass.localize("ui.components.logbook.from")} ${this.hass.localize("ui.components.logbook.event")} ${e.context_event_type}`}},{kind:"method",key:"_renderEntity",value:function(e,i){const r=e&&e in this.hass.states,n=i||r&&this.hass.states[e].attributes.friendly_name||e;return r?t.dy`<button
      class="link"
      @click=${this._entityClicked}
      .entityId=${e}
    >
      ${n}
    </button>`:n}},{kind:"method",key:"_formatMessageWithPossibleEntity",value:function(e,i,r,n){if(-1!==e.indexOf(".")){const r=e.split(" ");for(let e=0,n=r.length;e<n;e++)if(r[e]in this.hass.states){const n=r[e];if(i.includes(n))return"";i.push(n);const o=r.splice(e);return o.shift(),t.dy` ${r.join(" ")}
          ${this._renderEntity(n,this.hass.states[n].attributes.friendly_name)}
          ${o.join(" ")}`}}if(r&&r in this.hass.states){const o=this.hass.states[r].attributes.friendly_name;if(o&&e.endsWith(o))return i.includes(r)?"":(i.push(r),e=e.substring(0,e.length-o.length),t.dy` ${n?this.hass.localize(n):""}
        ${e} ${this._renderEntity(r,o)}`)}return e}},{kind:"method",key:"_entityClicked",value:function(e){const t=e.currentTarget.entityId;t&&(e.preventDefault(),e.stopPropagation(),(0,l.B)(this,"hass-more-info",{entityId:t}))}},{kind:"method",key:"_close",value:function(){setTimeout((()=>(0,l.B)(this,"closed")),500)}},{kind:"get",static:!0,key:"styles",value:function(){return[f.Qx,f.$c,f.k1,t.iv`
        :host([virtualize]) {
          display: block;
          height: 100%;
        }

        .rtl {
          direction: ltr;
        }

        .entry-container {
          width: 100%;
        }

        .entry {
          display: flex;
          width: 100%;
          line-height: 2em;
          padding: 8px 16px;
          box-sizing: border-box;
          border-top: 1px solid var(--divider-color);
        }

        .entry.no-entity,
        .no-name .entry {
          cursor: default;
        }

        .entry:hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .narrow:not(.no-icon) .time {
          margin-left: 32px;
        }

        .message-relative_time {
          display: flex;
          flex-direction: column;
        }

        .secondary {
          font-size: 12px;
          line-height: 1.7;
        }

        .secondary a {
          color: var(--secondary-text-color);
        }

        .date {
          margin: 8px 0;
          padding: 0 16px;
        }

        .narrow .date {
          padding: 0 8px;
        }

        .rtl .date {
          direction: rtl;
        }

        .icon-message {
          display: flex;
          align-items: center;
        }

        .no-entries {
          text-align: center;
          color: var(--secondary-text-color);
        }

        state-badge {
          margin-right: 16px;
          flex-shrink: 0;
          color: var(--state-icon-color);
        }

        .message {
          color: var(--primary-text-color);
        }

        .no-name .message:first-letter {
          text-transform: capitalize;
        }

        a {
          color: var(--primary-color);
        }

        .container {
          max-height: var(--logbook-max-height);
        }

        .container,
        lit-virtualizer {
          height: 100%;
        }

        lit-virtualizer {
          contain: size layout !important;
        }

        .narrow .entry {
          line-height: 1.5;
          padding: 8px;
        }

        .narrow .icon-message state-badge {
          margin-left: 0;
        }
      `]}}]}}),t.oi)}))}}]);
//# sourceMappingURL=b0faad5f.js.map