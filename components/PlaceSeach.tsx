async function getPlaceDetails(placeId: string | null): Promise<google.maps.places.Place | undefined> {
    if (!placeId) {
        return undefined;
    }
    
    const { Place } =  await google.maps.importLibrary("places") as google.maps.PlacesLibrary;
    // Use place ID to create a new Place instance.
    const place = new Place({
        id: placeId,
    });

    // Call fetchFields, passing the desired data fields.
    await place.fetchFields({ fields: ['displayName', 'formattedAddress', 'location', 'googleMapsURI', 'types', 'rating', 'userRatingCount'] })
    return place;
}

export default getPlaceDetails;