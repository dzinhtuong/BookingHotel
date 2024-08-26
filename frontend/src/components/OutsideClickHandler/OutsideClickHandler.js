import PropTypes from 'prop-types';
import { useEffect, useRef } from 'react';

const OutsideClickHandler = ({ children, onOutsideClick }) => {
    const wrapperRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
                onOutsideClick();
            }
        };

        // Attach the event listener on mount
        document.addEventListener('mousedown', handleClickOutside);

        // Detach the event listener on unmount
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [onOutsideClick]);

    return <div ref={wrapperRef}>{children}</div>;
};

OutsideClickHandler.propTypes = {
    children: PropTypes.any.isRequired,
    onOutsideClick: PropTypes.func.isRequired,
};

export default OutsideClickHandler;