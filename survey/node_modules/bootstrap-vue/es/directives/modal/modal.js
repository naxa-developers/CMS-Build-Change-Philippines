import target from '../../utils/target';
import { setAttr } from '../../utils/dom';

var listenTypes = { click: true };

export default {
  // eslint-disable-next-line no-shadow-restricted-names
  bind: function bind(el, binding, vnode) {
    target(vnode, binding, listenTypes, function (_ref) {
      var targets = _ref.targets,
          vnode = _ref.vnode;

      targets.forEach(function (target) {
        vnode.context.$root.$emit('bv::show::modal', target, vnode.elm);
      });
    });
    if (el.tagName !== 'BUTTON') {
      // If element is not a button, we add `role="button"` for accessibility
      setAttr(el, 'role', 'button');
    }
  }
};