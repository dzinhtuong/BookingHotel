import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { convertDateToMmDmYyyy } from '../utils/func';
import SearchGroup from '../components/SearchGroup';
import img1 from '../assets/images/hcm.jpg';
import img2 from '../assets/images/seoul.jpeg';
import DestinationList from '../components/DestinationList';

const HomePage = () => {
    const { t } = useTranslation();
    const [destination, setDestination] = useState('');
    const [startDate, setStartDate] = useState(convertDateToMmDmYyyy(new Date()));
    const [endDate, setEndDate] = useState(convertDateToMmDmYyyy(new Date()));
    const [countRoom, setCountRoom] = useState(1);
    const [countAdult, setCountAdult] = useState(1);
    const [countChild, setCountChild] = useState(0);

    const [domesticDes, setDomesticDes] = useState([]);
    const [foreignDes, setForeignDes] = useState([]);


    const handleSearch = () => {
        let data = {
            destination: destination,
            startDate: startDate,
            endDate: endDate,
            countRoom: countRoom,
            countAdult: countAdult,
            countChild: countChild,
        };
        console.log(data);
    };

    useEffect(() => {
        setTimeout(() => {
            setDomesticDes([
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
                { destination: 'Hồ Chí Minh', image: img1, numHouse: 15556 },
            ]);
            setForeignDes([
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
                { destination: 'Seoul', image: img2, numHouse: 17556 },
            ]);
        }, 2000);
    }, []);

    return (
        <>
            <SearchGroup
                destination={destination}
                setDestination={setDestination}
                startDate={startDate}
                setStartDate={setStartDate}
                endDate={endDate}
                setEndDate={setEndDate}
                countRoom={countRoom}
                setCountRoom={setCountRoom}
                countAdult={countAdult}
                setCountAdult={setCountAdult}
                countChild={countChild}
                setCountChild={setCountChild}
                handleSearch={handleSearch}
            />
            <DestinationList title={t('Các điểm đến thu hút nhất Việt Nam')} destinations={domesticDes}/>
            <DestinationList title={t('Các điểm đến nổi tiếng ngoài Việt Nam')} destinations={foreignDes}/>
        </>
    );
};

export default HomePage;
