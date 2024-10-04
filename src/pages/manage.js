import React, { useState } from 'react';
import Header from '../components/header';
import { Spinner } from 'flowbite-react';

const Manage = () => {
    const [isLoading] = useState(true);
   
    return (
        <div className='h-screen flex flex-col'>
            <Header isHome={true} className="sticky top-0 z-50" />
            <div className='dark:bg-black flex-1'>
                <div className='flex-1 flex flex-col items-center justify-center py-8'>
                    {isLoading && <>
                        <div className="text-center py-10 w-screen flex items-center justify-center">
                            <Spinner size="xl" className='fill-black dark:fill-white' />
                        </div>
                    </>}
                </div>
            </div>
        </div>
    );
};

export default Manage;
