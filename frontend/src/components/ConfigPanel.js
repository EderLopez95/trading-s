import { useState, useEffect, useContext } from "react";
import { getConfig, saveConfig, getSymbols } from "../services/api";
import "./ConfigPanel.scss";
import AsyncSelect from "react-select/async";
import { AppContext } from "../App";
import { StrategyType } from "../enums";

function ConfigPanel() {
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState({});
  const { showToast, config, setConfig, selectedConfig, setSelectedConfig } = useContext(AppContext);

  useEffect(() => {
    if (config)
      setLoading(false);
  }, []);

  const loadSymbols = async (inputValue) => {
    try {
      const data = await getSymbols(inputValue);
      return data.map((s) => ({
        value: s,
        label: s
      }));
    } catch (error) {
      console.error("Error loading symbols:", error);
      return [];
    }
  };

  const parseSymbols = (symbols) => {
    if (!symbols) return [];
    if (Array.isArray(symbols)) {
      return symbols.map((s) => ({
        value: s,
        label: s
      }));
    }
    return symbols.split(",").map((s) => ({
      value: s.trim(),
      label: s.trim()
    }));
  };

  // const handleTimeframeChange = (type, value) => {
  //   setConfig({
  //     ...config,
  //     timeframes: {
  //       ...config.timeframes,
  //       [type]: value
  //     }
  //   });
  // };

  const validateConfig = () => {
    const newErrors = {};

    const symbolsArray =
      typeof config.symbols === "string"
        ? config.symbols.split(",").filter(s => s.trim() !== "")
        : config.symbols;

    if (!symbolsArray || symbolsArray.length === 0) {
      newErrors.symbols = "At least one symbol is required";
    }

    if (!config.strategy) {
      newErrors.strategy = "Select a strategy";
    }

    if (!config.timeframes?.trend) {
      newErrors.trend = "Trend timeframe required";
    }

    if (!config.timeframes?.entry) {
      newErrors.entry = "Entry timeframe required";
    }

    if (
      config.timeframes?.trend &&
      config.timeframes?.entry &&
      config.timeframes.trend === config.timeframes.entry
    ) {
      newErrors.entry = "Trend and Entry timeframes must be different";
    }

    if (!config.execution_interval || config.execution_interval < 10) {
      newErrors.execution_interval = "Execution interval must be greater or equal to 10";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSaveConfig = async () => {
    if (!validateConfig()) {
      showToast("error", "Fix form errors before saving");
      return;
    }

    try {
      let updatedConfigs;

      if (selectedConfig.id) {
        // update
        updatedConfigs = config.configurations.map(c =>
          c.id === selectedConfig.id ? selectedConfig : c
        );
      } else {
        // create
        updatedConfigs = [
          ...config.configurations,
          {
            ...selectedConfig,
            id: crypto.randomUUID().slice(0, 8),
            enabled: true
          }
        ];
      }
  
      const newConfig = {
        ...config,
        configurations: updatedConfigs
      };

      const response = await saveConfig(newConfig);

      if (response.success) {
        showToast("info", "Config saved successfully");
        setConfig(newConfig);
        setSelectedConfig(null);
      } else {
        const msg = response.errors?.[0]?.msg || "Invalid config";
        showToast("error", msg);
      }
    } catch (error) {
      console.error("Error saving configuration:", error);
      showToast("error", "Error saving configuration");
    }
  };

  const validateConfigInterval = () => {
    const newErrors = {};
    
    if (!config.execution_interval || config.execution_interval < 30) {
      newErrors.execution_interval = "Execution interval must be greater or equal to 30";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSaveInterval = async () => {
    if (!validateConfigInterval()) {
      showToast("error", "Fix form errors before saving");
      return;
    }

    try {    
      const newConfig = {
        ...config,
        execution_interval: config.execution_interval
      };
      
      const response = await saveConfig(newConfig);

      if (response.success) {
        showToast("info", "Interval saved successfully");
        setConfig(newConfig);
      } else {
        const msg = response.errors?.[0]?.msg || "Invalid interval";
        showToast("error", msg);
      }
    } catch (error) {
      console.error("Error saving interval:", error);
      showToast("error", "Error saving interval");
    }
  };

  if (loading) return <div className="loading-warning">Loading configuration...</div>;
  if (!config) return <div className="loading-warning">Error loading configuration</div>;

  return (
    <>
      <div className="config-panel">
        <div className="config-title">
          Add or update configuration
        </div>
        <div className="field">
          <label>Symbols:</label>
          <AsyncSelect
              isMulti
              cacheOptions
              isSearchable
              closeMenuOnSelect={false}
              defaultOptions={false}
              loadOptions={loadSymbols}            
              onChange={(selected) => {
                const symbols = selected?.map(s => s.value) || [];
                setSelectedConfig({ ...selectedConfig, symbols });
              }}
              // value={parseSymbols(config.symbols)}
              // onChange={(selected) => {
              //   if (!selected) {
              //     setConfig({ ...config, symbols: "" });
              //     return;
              //   }
              //   const unique = [...new Set(selected.map((s) => s.value))].sort();
              //   const symbolsString = unique.join(", ");
              //   setConfig({
              //     ...config,
              //     symbols: symbolsString
              //   });
              // }}
              placeholder="Select symbols..."
              classNamePrefix={"symbol-select"}
            />
            {/* {errors.symbols && <span className="error">{errors.symbols}</span>} */}
        </div>
        <div className="field">
          <label>Strategy:</label>
          <AsyncSelect
              isMulti
              closeMenuOnSelect={false}
              defaultOptions={false}
              loadOptions={loadSymbols}            
              onChange={(selected) => {
                const symbols = selected?.map(s => s.value) || [];
                setSelectedConfig({ ...selectedConfig, symbols });
              }}
              placeholder="Select strategies..."
              classNamePrefix={"symbol-select"}
            />
          {/* <select
            // value={config.strategy}
            // onChange={(e) =>
            //   setConfig({
            //     ...config,
            //     strategy: e.target.value
            //   })
            // }
          >
            <option value={StrategyType.MULTI_SMA}>{StrategyType.MULTI_SMA_value}</option>
            <option value={StrategyType.RSI_CROSS_TREND}>{StrategyType.RSI_CROSS_TREND_value}</option>
          </select> */}
          {/* {errors.strategy && <span className="error">{errors.strategy}</span>} */}
        </div>
        <div className="field">
          <label>Timeframe Trend:</label>
          <select          
            onChange={(e) =>
              setSelectedConfig({
                ...selectedConfig,
                timeframes: { ...selectedConfig.timeframes, trend: e.target.value }
              })
            }
            // value={config.timeframes.trend}
            // onChange={(e) =>
            //   handleTimeframeChange("trend", e.target.value)
            // }
          >
            <option value="M5">M5</option>
            <option value="M15">M15</option>
            <option value="H1">H1</option>
            <option value="H4">H4</option>
            <option value="D1">D1</option>
            <option value="W1">W1</option>
          </select>
          {/* {errors.trend && <span className="error">{errors.trend}</span>} */}
        </div>
        <div className="field">
          <label>Timeframe Entry:</label>
          <select          
            onChange={(e) =>
              setSelectedConfig({
                ...selectedConfig,
                timeframes: { ...selectedConfig.timeframes, entry: e.target.value }
              })
            }
            // value={config.timeframes.entry}
            // onChange={(e) =>
            //   handleTimeframeChange("entry", e.target.value)
            // }
          >
            <option value="M5">M5</option>
            <option value="M15">M15</option>
            <option value="H1">H1</option>
            <option value="H4">H4</option>
            <option value="D1">D1</option>
            <option value="W1">W1</option>
          </select>
          {/* {errors.entry && <span className="error">{errors.entry}</span>} */}
        </div>
        <div className="actions">
          <button onClick={handleSaveConfig}>
            Save
          </button>
        </div>
      </div>
      <div className="config-panel">
        <div className="config-title">
          Update interval
        </div>
        <div className="field">
          <label>Execution interval (seconds):</label>
          <input
            type="number"
            min={30}
            value={config.execution_interval || ""}
            onChange={(e) => {
              setConfig({
                ...config,
                execution_interval: parseInt(e.target.value) || 0
              });
            }}
          />
          {errors.execution_interval && (
            <span className="error">{errors.execution_interval}</span>
          )}
        </div>
        <div className="actions">
          <button onClick={handleSaveInterval}>
            Save
          </button>
        </div>
      </div>
    </>
  );
}

export default ConfigPanel;
