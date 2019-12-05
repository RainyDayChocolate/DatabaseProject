DataBase Schema Structure and Update

+ FlightDelay Dataset

  + ormalization
    + Location(City, State, StateAbbrivate)
    + Airport(**AirportId, LocationID**)（JFK, New York City, NY） _Some airports would serves many cities around it_.
    + Flight(**FlightNum, Depature\_Airport, Arrive\_Airport**, Carrier)
    + DelayReasons(**ReasonId**, Reason)
    + FlightTimeTable(**ID**, Date, Flight\_Num, Depature\_Airport, Depature\_Time, Arrive\_Airport, Arrive\_Time, Crs_elapsed_time, Actual_elapsed_time)
    + DelayTime(**ID**, **ReasonID **, Delay\_Time)
  + Constraint
    + **Airport** LocationId $\rightarrow$Location **LocationId**
    + **DelayTime** Id $\rightarrow$ **FlightTimeTable** ID
    + **DelayTime** ReasonID$\rightarrow$ **DelayReasons**.ReasonID
    + **FlightTimeTable**.Depature\_Airport,  Arrive\_Airport$\rightarrow$ Airport.ID

+ Gun Violence Dataset

  + Normalization

    + Location(Reuse Flight Dataset Location)

    + Incident(**Id**, LocationId, gDate,  address, n\_killed, n\_injured, gun\_stolen, gun\_type, n_guns_involved, participants：

      [{'**name**': XX, '**gender**': XX, '**Age**': XX, '**Age_Group**': XX, '**type**': victim or suspect,

      ​	,'Status': [Arrest, Injuried, Dead...]}, ...]

      **Part of NonRelationship Database**

  + Constraint

    + Gender, Type, Status should be fall in Enumerates
    + Injured, n_killed should less than the amount of participants.
    + Participants should not be empty.

+ Weather

  + Normalization
    + Weather(**LocationId**, **Date**, Humidity, Pressure, Temperature, Wind_Speed, Wind_Direction, Weather_Description)
  + Constraint
    + State, City should be restricted in Location
    + Temperature, Wind_Speed should not be negative.

+ Accident

  + Normalization
    + Location(Reuse Flight Dataset Location)
    + Accident(**ID**, **LocationId**, Severity, Start_Time, End_Time, Distance, Street, Side, Visibility, Sunrise_Sunset)
    + Annotations(**AnnaotationID**, Annotation)
    + POI_annotation(**ID**, AnnaotationID)
  + Constraint
    + POI_annotation.AnnaotationID should be fall in Annotations
    + Source 

  