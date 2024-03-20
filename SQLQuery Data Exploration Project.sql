/*
Covid 19 DATA EXPLORATION 

Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types

*/
SELECT * FROM [portfolio project].dbo.['owid-covid-data 1$']
order by 3, 4

--SELECT * FROM [portfolio project].dbo.['owid-covid-data 1$']
--order by 3,4

select location, date, total_cases, new_cases, total_deaths, population
from [portfolio project].dbo.['owid-covid-data 1$']
order by 1, 2


--looking total cases and total deaths
select location, date, total_cases, total_deaths, population
from [portfolio project].dbo.['owid-covid-data 1$']
order by 1, 2

-- Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in your country

select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from [portfolio project].dbo.['owid-covid-data 1$']
where location like '%United States%'
order by 1, 2

-- Total Cases vs Population
-- Shows what percentage of population infected with Covid

Select Location, date, Population, total_cases,  (total_cases/population)*100 as PercentPopulationInfected
From [portfolio project].dbo.['owid-covid-data 1$']
--Where location like '%United states%'
order by 1,2


-- Countries with Highest Infection Rate compared to Population

Select Location, Population, MAX(total_cases) as HighestInfectionCount,  Max((total_cases/population))*100 as PercentPopulationInfected
From [portfolio project].dbo.['owid-covid-data 1$']
--Where location like '%states%'
Group by Location, Population
order by PercentPopulationInfected desc

-- Countries with Highest Death Count per Population

Select Location, MAX(cast(Total_deaths as int)) as TotalDeathCount
From [portfolio project].dbo.['owid-covid-data 1$']
--Where location like '%states%'
Where continent is not null 
Group by Location
order by TotalDeathCount desc

-- BREAKING THINGS DOWN BY CONTINENT

-- Showing contintents with the highest death count per population
Select continent, MAX(cast(Total_deaths as int)) as TotalDeathCount
From [portfolio project].dbo.['owid-covid-data 1$']
--Where location like '%states%'
Where continent is not null 
Group by continent
order by TotalDeathCount desc


-- GLOBAL NUMBERS

Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(New_Cases)*100 as DeathPercentage
From [portfolio project].dbo.['owid-covid-data 1$']
--Where location like '%states%'
where continent is not null 
--Group By date
order by 1,2



-- Total Population vs Vaccinations
-- Shows Percentage of Population that has recieved at least one Covid Vaccine

Select continent, location, date, population, new_vaccinations
, SUM(CONVERT(int, new_vaccinations)) OVER (Partition by location Order by location, Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From [portfolio project].dbo.['owid-covid-data 1$']
where continent is not null 
order by 2,3



-- Using CTE to perform Calculation on Partition By in previous query

With PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
Select continent, location, date, population, new_vaccinations
, SUM(CONVERT(int, new_vaccinations)) OVER (Partition by location Order by location, Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From [portfolio project].dbo.['owid-covid-data 1$']

where continent is not null 
--order by 2,3
)
Select *, (RollingPeopleVaccinated/Population)*100
From PopvsVac


-- Using Temp Table to perform Calculation on Partition By in previous query

DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)


Insert into #PercentPopulationVaccinated
Select continent, location, date, population, new_vaccinations
, SUM(CONVERT(int, new_vaccinations)) OVER (Partition by location Order by location, Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From [portfolio project].dbo.['owid-covid-data 1$']

--where dea.continent is not null 
--order by 2,3

Select *, (RollingPeopleVaccinated/Population)*100
From #PercentPopulationVaccinated



-- Creating View to store data for later visualizations

Create View PercentPopulationVaccinated as
Select continent, location, date, population, new_vaccinations
, SUM(CONVERT(int, new_vaccinations)) OVER (Partition by location Order by location, Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From [portfolio project].dbo.['owid-covid-data 1$']

where continent is not null 
