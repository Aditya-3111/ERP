import Icon from './Icon.jsx';

const VARIANTS = { primary: 'btn-primary', secondary: 'btn-secondary', danger: 'btn-danger', ghost: 'btn-ghost' };

/** <Button variant="primary" icon="plus" loading={saving} onClick={...}>Save</Button> */
export default function Button({ variant = 'primary', size, icon, loading = false, className = '', children, type = 'button', ...rest }) {
  const classes = ['btn', VARIANTS[variant] || VARIANTS.primary, size === 'sm' ? 'btn-sm' : '', className].join(' ');
  return (
    <button type={type} className={classes} disabled={loading || rest.disabled} {...rest}>
      {loading ? <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" /> : icon && <Icon name={icon} className="h-4 w-4" />}
      {children}
    </button>
  );
}
