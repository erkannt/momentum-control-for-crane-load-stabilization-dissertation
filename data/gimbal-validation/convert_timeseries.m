% Convert Timeseries to Vectors
%
% Loads all .mat files in folder, extracts timestamps into new variable,
% overwrites TS-Variable with new variable that only contains the data from
% the timeseries.

clear;
matfiles = dir('*.mat');

for i = 1:length(matfiles)
    clearvars -except matfiles i
    matfiles(i).name;
    load(matfiles(i).name);
    ws = whos;
    for j = 1:length(ws)
        if strcmp(ws(j).class, 'timeseries')
            eval(['time = ' ws(j).name '.Time;']);
            eval(['tsdata = ' ws(j).name '.Data;']);
            eval(['clearvars ' ws(j).name])
            genvarname(ws(j).name);
            eval([ws(j).name '= tsdata;']);
        end
    end
    filename = strrep(matfiles(i).name, '.mat', '__convertedTimeseries.mat');
    save(filename);
end