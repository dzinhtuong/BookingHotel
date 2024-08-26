import PropTypes from 'prop-types'

const DatePicker = ({styles, date, setDate}) => {
    return (
        <input
            type="date"
            className={`cursor-pointer bg-white border border-gray-300 text-gray-900 text-base rounded-lg focus:outline-primary block w-full ${styles}`}
            defaultValue={date}
            onChange={(e)=> setDate(e.target.value)}
        />
    );
};

DatePicker.propTypes = {
    styles: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    setDate: PropTypes.func.isRequired,
}

export default DatePicker;
