import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Scrollbar, A11y } from 'swiper/modules';
import PropTypes from 'prop-types';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';
import Destination from '../components/Destination';

const DestinationList = ({ title, destinations }) => {
    return (
        <div className="w-full h-[300px] p-[24px] m-auto mb-[48px] bg-white xl:w-1200">
            <div className="text-center text-[24px] text-[#2a2a2e] font-medium pb-[8px]">{title}</div>
            <Swiper
                spaceBetween={0}
                modules={[Navigation, Pagination, Scrollbar, A11y]}
                pagination={{ clickable: true }}
                onSlideChange={() => console.log('slide change')}
                onSwiper={(swiper) => console.log(swiper)}
                breakpoints={{
                    0: {
                        slidesPerView: 2,
                    },
                    768: {
                        slidesPerView: 5,
                    },
                    1280: {
                        slidesPerView: 7,
                    },
                }}
            >
                {destinations &&
                    destinations.map((destination, index) => (
                        <SwiperSlide key={index}>
                            <Destination destination={destination} />
                        </SwiperSlide>
                    ))}
            </Swiper>
        </div>
    );
};

DestinationList.propTypes = {
    title: PropTypes.string.isRequired,
    destinations: PropTypes.any,
};


export default DestinationList;
