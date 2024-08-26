import { Trans } from 'react-i18next';
import { Link } from 'react-router-dom';

const Policy = () => {
    return (
        
            <div className="text-[12px] text-[#2a2a2e] text-center my-[32px]">
                <Trans i18nKey="policy">
                    Khi đăng nhập, tôi đồng ý với các <Link to="#" className="text-[12px] text-primary"> Điều khoản sử dụng </Link> và <Link to="# " className="text-[12px] text-primary"> Chính sách bảo mật</Link> của Booking.
                </Trans>
            </div>
        
    )
}

export default Policy;