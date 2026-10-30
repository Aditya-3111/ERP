// All icons in one place. Use:  <Icon name="users" className="h-5 w-5" />
// (icons come from the free "Lucide" set inside the react-icons package)
import {
  LuLayoutDashboard, LuLandmark, LuPackage, LuHandshake, LuUsers, LuDoorOpen, LuShoppingCart,
  LuFactory, LuWrench, LuSettings, LuLogOut, LuMenu, LuPlus, LuPencil, LuTrash2, LuSearch, LuX,
  LuChevronDown, LuChevronRight, LuChevronLeft, LuFileText, LuReceipt, LuScale, LuTrendingUp,
  LuWallet, LuTriangleAlert, LuCircle, LuCheck, LuInfo, LuRefreshCw, LuUser, LuKeyRound,
  LuBuilding2, LuBox, LuClipboardList, LuEye, LuArrowRightLeft, LuCalendarDays,
} from 'react-icons/lu';

const ICONS = {
  dashboard: LuLayoutDashboard, finance: LuLandmark, inventory: LuPackage, crm: LuHandshake,
  hr: LuUsers, gate: LuDoorOpen, pos: LuShoppingCart, production: LuFactory, maintenance: LuWrench,
  admin: LuSettings, logout: LuLogOut, menu: LuMenu, plus: LuPlus, edit: LuPencil, trash: LuTrash2,
  search: LuSearch, close: LuX, down: LuChevronDown, right: LuChevronRight, left: LuChevronLeft,
  file: LuFileText, receipt: LuReceipt, scale: LuScale, trend: LuTrendingUp, wallet: LuWallet,
  warning: LuTriangleAlert, check: LuCheck, info: LuInfo, refresh: LuRefreshCw, user: LuUser,
  key: LuKeyRound, building: LuBuilding2, box: LuBox, list: LuClipboardList, view: LuEye,
  move: LuArrowRightLeft, calendar: LuCalendarDays,
};

export default function Icon({ name, className = 'h-5 w-5' }) {
  const Component = ICONS[name] || LuCircle;
  return <Component className={className} aria-hidden="true" />;
}
