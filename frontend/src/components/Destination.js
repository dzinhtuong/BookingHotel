import PropTypes from 'prop-types';
import { useTranslation } from 'react-i18next'

const Destination = ({destination}) => {
    const { t } = useTranslation();
    return (
        <div className="flex items-center flex-col py-[16px] cursor-pointer">
            <img
                src={destination.image}
                alt=""
                className="mb-[12px] w-[124px] h-[124px] rounded-full border border-solid border-[#dddfe2] transform transition duration-300 hover:scale-110 hover:shadow-lg"
            />
            <div className="text-[16px] text-[#2a2a2e]">{destination.destination}</div>
            <div className="text-[12px] text-[#737373]">{destination.numHouse} {t('chỗ ở')}</div>
        </div>
    );
};

Destination.propTypes = {
    destination: PropTypes.object.isRequired,
};

export default Destination;
