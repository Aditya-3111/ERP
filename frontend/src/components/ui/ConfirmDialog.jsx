import Button from './Button.jsx';
import Modal from './Modal.jsx';

export default function ConfirmDialog({ title = 'Are you sure?', message, confirmLabel = 'Delete', loading, onConfirm, onCancel }) {
  return (
    <Modal title={title} onClose={onCancel} size="md" footer={
      <>
        <Button variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button variant="danger" loading={loading} onClick={onConfirm}>{confirmLabel}</Button>
      </>
    }>
      <p className="text-sm text-slate-600">{message}</p>
    </Modal>
  );
}
