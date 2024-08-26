import { useTranslation } from 'react-i18next'
import PropTypes from 'prop-types';

import beachVid from '../../assets/videos/beachVid.mp4';
import SearchInputText from '../../components/SearchGroup/SearchInputText';
import DatePicker from '../../components/SearchGroup/DatePicker';
import SearchOptions from '../../components/SearchGroup/SearchOptions';

const SearchGroup = (props) => {
    const { t } = useTranslation();
    return (
        <div className="relative w-full h-search-group">
            <video className="w-full h-full object-cover" src={beachVid} autoPlay loop muted />
            <div className="absolute top-0 bottom-0 left-[16px] right-[16px] m-auto flex flex-col justify-center items-center xl:w-1200 xl:left-0 xl:right-0">
                <div className="text-xl text-center font-semibold mb-4 text-white md:text-3xl xl:text-3xl">
                    {t("RONG CHƠI BỐN PHƯƠNG, GIÁ VẪN \"YÊU THƯƠNG\"")}
                </div>
                <form className="w-full p-[24px] rounded-3xl shadow-2xl bg-[#f8f7f9] md:p-[48px] xl:p-[48px]">
                    <div className="mb-[16px]">
                        <SearchInputText
                            styles="p-6 pl-[40px]"
                            destination={props.destination}
                            setDestination={props.setDestination}
                        />
                    </div>
                    <div className="mb-[42px] grid grid-cols-2 gap-4">
                        <div className="col-span-2 grid grid-cols-2 gap-3 md:col-span-1 xl:col-span-1">
                            <DatePicker styles="p-6" date={props.startDate} setDate={props.setStartDate} />
                            <DatePicker styles="p-6" date={props.endDate} setDate={props.setEndDate} />
                        </div>
                        <div className="relative col-span-2 md:col-span-1 xl:col-span-1">
                            <SearchOptions
                                countRoom={props.countRoom}
                                setCountRoom={props.setCountRoom}
                                countAdult={props.countAdult}
                                setCountAdult={props.setCountAdult}
                                countChild={props.countChild}
                                setCountChild={props.setCountChild}
                            />
                        </div>
                    </div>
                    <div className="flex justify-center items-center">
                        <div
                            onClick={props.handleSearch}
                            className="p-3 text-white bg-primary rounded cursor-pointer text-center hover:opacity-80 w-[490px] h-[64px] flex justify-center items-center text-[20px] "
                        >
                            {t('TÌM KIẾM')}
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
};

SearchGroup.propTypes = {
    destination: PropTypes.any.isRequired,
    setDestination: PropTypes.func.isRequired,
    startDate: PropTypes.any.isRequired,
    setStartDate: PropTypes.func.isRequired,
    endDate: PropTypes.any.isRequired,
    setEndDate: PropTypes.func.isRequired,
    countRoom: PropTypes.any.isRequired,
    setCountRoom: PropTypes.func.isRequired,
    countAdult: PropTypes.any.isRequired,
    setCountAdult: PropTypes.func.isRequired,
    countChild: PropTypes.any.isRequired,
    setCountChild: PropTypes.func.isRequired,
    handleSearch: PropTypes.func.isRequired,
};

export default SearchGroup;
