import PropTypes from 'prop-types';

const TextInput = ({ label, onChange }) => {
    return (
        <>
            <label className="block mb-2 font-medium text-gray-900">{label}</label>
            <input
                type="text"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:outline-primary block w-full p-[12px]"
                placeholder={label}
                onChange={onChange}
            />
        </>
    );
};

TextInput.propTypes = {
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func,
};

export default TextInput;
